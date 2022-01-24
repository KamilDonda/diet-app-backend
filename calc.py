import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix, classification_report
import db


def get_user_classification(calories):
    small = 2200
    large = 2800

    if(calories <= small):
        return -1
    if(calories >= large):
        return 1
    return 0


def load_rules():
    data = pd.read_csv('./src/diet_calculator/test_data/rules.csv')
    return data


def load_user_rules():
    # Zmienic sciezke
    data = pd.read_csv('./src/diet_calculator/test_data/rules-user.csv')
    return data


# pobranie z bazy, podzielenie 80/20
# train_test_proportion = 0.8
def calculate_system():
    columns = ["Meal ID", "Calories", "Fat",
            "Carbohydrates", "Protein", "Classification"]
    type_dict = {'Meal ID': 'int32', 'Calories': 'float', 'Fat': 'float',
                'Carbohydrates': 'float', 'Protein': 'float', 'Classification': 'object'}
    all_data = np.array(db.get_all_meals_with_nutriments())
    np.random.shuffle(all_data)
    test_arr = []
    arr = []

    for meal in all_data:
        if meal[5] == 'None':
            meal[5] = np.nan
            arr.append(meal)
        else:
            test_arr.append(meal)

    test_arr = np.array(test_arr)
    arr = np.array(arr)

    df_test = pd.DataFrame(test_arr, columns=columns).astype(type_dict)
    df = pd.DataFrame(arr, columns=columns).astype(type_dict)
    # zbiór testowy: posiłki, które mają klasyfikację
    # zbiór treningowy: posiłki, które nie mają klasyfikacji

    rules = load_rules()


    def histogram():
        for column in df.columns[1:]:
            plt.figure(figsize=(9, 6))
            plt.hist(df[column])
            plt.ylabel('Prawdopodobieństwo')
            plt.xlabel(column)
            plt.show()

    # histogram()


    for column in df.columns[1:-1]:
        fig, axes = plt.subplots(figsize=(9, 5))
        fig.suptitle(column)

        minimum = df[column].min()
        maximum = df[column].max()
        mid = (maximum + minimum) / 2

        stdev = np.linspace(minimum, maximum, 1000).std()

        norm_min = stats.norm(loc=minimum, scale=stdev)
        norm_mid = stats.norm(loc=mid, scale=stdev)
        norm_max = stats.norm(loc=maximum, scale=stdev)

        sigma = stdev * 5
        scalar = MinMaxScaler()

        x = np.linspace(minimum - sigma, minimum + sigma, 1000)
        min_scalar = scalar.fit(norm_min.pdf(x).reshape(-1, 1))
        axes.plot(x, min_scalar.transform(norm_min.pdf(x).reshape(-1, 1)))

        x = np.linspace(mid - sigma, mid + sigma, 1000)
        mid_scalar = scalar.fit(norm_mid.pdf(x).reshape(-1, 1))
        axes.plot(x, mid_scalar.transform(norm_mid.pdf(x).reshape(-1, 1)))

        x = np.linspace(maximum - sigma, maximum + sigma, 1000)
        max_scalar = scalar.fit(norm_max.pdf(x).reshape(-1, 1))
        axes.plot(x, max_scalar.transform(norm_max.pdf(x).reshape(-1, 1)))

        def small_pdf(value, scal=min_scalar, norm=norm_min):
            result = scal.transform(norm.pdf(value).reshape(-1, 1))
            if result < 0:
                return 0
            elif result > 1:
                return 1
            return result[0][0]

        def normal_pdf(value, scal=mid_scalar, norm=norm_mid):
            result = scal.transform(norm.pdf(value).reshape(-1, 1))
            if result < 0:
                return 0
            elif result > 1:
                return 1
            return result[0][0]

        def large_pdf(value, scal=max_scalar, norm=norm_max):
            result = scal.transform(norm.pdf(value).reshape(-1, 1))
            if result < 0:
                return 0
            elif result > 1:
                return 1
            return result[0][0]

        axes.set_title("\nmin:%d, mid:%s, max:%d" %
                    (round(minimum, 2), round(mid, 2), round(maximum, 2)))

        df.insert(0, f'{column} small pdf', small_pdf, True)
        df.insert(0, f'{column} normal pdf', normal_pdf, True)
        df.insert(0, f'{column} large pdf', large_pdf, True)


    plt.tight_layout(pad=2)
    # plt.show()


    def calc_membership(calories, fat, carbo, protein):
        values = [calories, fat, carbo, protein]
        result = []
        for column, value in zip(["Calories", "Fat", "Carbohydrates", "Protein"], values):
            small_pdf = df[f'{column} small pdf'].iloc[0]
            normal_pdf = df[f'{column} normal pdf'].iloc[0]
            large_pdf = df[f'{column} large pdf'].iloc[0]

            small = small_pdf(value)
            normal = normal_pdf(value)
            large = large_pdf(value)

            if small > normal and small > large:
                result.append((column, 'min', small))
            elif normal > small and normal > large:
                result.append((column, 'mid', normal))
            else:
                result.append((column, 'max', large))

        return result


    def get_classification(rules, calories, fat, carbo, protein):
        membership = calc_membership(calories, fat, carbo, protein)
        print(membership)

        membership_calc = membership[0][1]
        membership_fat = membership[1][1]
        membership_carbo = membership[2][1]
        membership_protein = membership[3][1]

        rule = rules[(rules['Kalorie'] == membership_calc) &
                    (rules['Tłuszcz'] == membership_fat) &
                    (rules['Węglowodany'] == membership_carbo) &
                    (rules['Białko'] == membership_protein)]

        print(rule['Dieta'].values[0])
        return rule['Dieta'].values[0]


    y_preds_series = df_test.apply(lambda row: get_classification(rules,
                                                                row['Calories'],
                                                                row['Fat'],
                                                                row['Carbohydrates'],
                                                                row['Protein'],
                                                                ), axis=1)


    def plot_cm(y_true, y_pred, labels):
        from sklearn.metrics._plot.confusion_matrix import ConfusionMatrixDisplay

        sample_weight = None
        normalize = None
        include_values = True
        cmap = 'viridis'
        ax = None
        xticks_rotation = 'horizontal'
        values_format = None

        cm = confusion_matrix(y_true, y_pred, sample_weight=sample_weight,
                            labels=labels, normalize=normalize)
        display_labels = labels

        disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                    display_labels=display_labels)
        return disp.plot(include_values=include_values,
                        cmap=cmap, ax=ax, xticks_rotation=xticks_rotation,
                        values_format=values_format)


    y_true = df_test['Classification'].to_numpy(dtype='int32')
    y_preds = y_preds_series.to_numpy(dtype='int32')

    plot_cm(y_true, y_preds, [-1, 0, 1])
    print(classification_report(y_true, y_preds))

# print(calculate_system())