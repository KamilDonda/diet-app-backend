import input
import calc
from scipy import stats
import numpy as np
from sklearn.preprocessing import MinMaxScaler

user_calories, user_proteins, user_fats, user_carbs = input.calcInput(
    True, 22, 70, 175, 2, 2, 'Preferences')

df = calc.load_data_pandas()
# print(df)

calories = df['Calories']
proteins = df['Protein']
fats = df['Fat']
carbs = df['Carbohydrates']

# print(calories)

min = min(calories)
max = max(calories)
mid = (max + min) / 2

# print(min)
# print(max)
# print(mid)

stdev = np.linspace(min, max, 1000).std()

norm_min = stats.norm(loc=min, scale=stdev)
norm_mid = stats.norm(loc=mid, scale=stdev)
norm_max = stats.norm(loc=max, scale=stdev)

sigma = stdev * 5
scalar = MinMaxScaler()

x = np.linspace(min - sigma, min + sigma, 1000)
min_scalar = scalar.fit(norm_min.pdf(x).reshape(-1, 1))
# min_scalar = min_scalar.transform(norm_min.pdf(x).reshape(-1, 1))

x = np.linspace(mid - sigma, mid + sigma, 1000)
mid_scalar = scalar.fit(norm_mid.pdf(x).reshape(-1, 1))
# mid_scalar = mid_scalar.transform(norm_mid.pdf(x).reshape(-1, 1))

x = np.linspace(max - sigma, max + sigma, 1000)
max_scalar = scalar.fit(norm_max.pdf(x).reshape(-1, 1))
# max_scalar = max_scalar.transform(norm_max.pdf(x).reshape(-1, 1))

# print('min_scalar')
# print(min_scalar)
# print('mid_scalar')
# print(mid_scalar)
# print('max_scalar')
# print(max_scalar)


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

result = []

for i in range(len(calories)):
    small = small_pdf(calories[i])
    normal = normal_pdf(calories[i])
    large = large_pdf(calories[i])

    if small > normal and small > large:
        result.append(('cal', 'min', small))
    elif normal > small and normal > large:
        result.append(('cal', 'mid', normal))
    else:
        result.append(('cal', 'max', large))

for i in result:
    print(i)