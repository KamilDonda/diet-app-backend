import pandas as pd
from scipy import stats
import numpy as np
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

def load_data_pandas():
    data = pd.read_csv('dane.csv', engine='python', sep=';')
    data = data.drop(columns=[])
    return data

def gaussian(data, name):
    minimum = min(data)
    maximum = max(data)
    mid = (maximum + minimum) / 2

    stdev = np.linspace(minimum, maximum, 1000).std()

    norm_min = stats.norm(loc=minimum, scale=stdev)
    norm_mid = stats.norm(loc=mid, scale=stdev)
    norm_max = stats.norm(loc=maximum, scale=stdev)

    sigma = stdev * 5
    scalar = MinMaxScaler()

    x = np.linspace(minimum - sigma, minimum + sigma, 1000)
    min_scalar = scalar.fit(norm_min.pdf(x).reshape(-1, 1))

    x = np.linspace(mid - sigma, mid + sigma, 1000)
    mid_scalar = scalar.fit(norm_mid.pdf(x).reshape(-1, 1))

    x = np.linspace(maximum - sigma, maximum + sigma, 1000)
    max_scalar = scalar.fit(norm_max.pdf(x).reshape(-1, 1))

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

    for i in range(len(data)):
        small = small_pdf(data[i])
        normal = normal_pdf(data[i])
        large = large_pdf(data[i])

        if small > normal and small > large:
            result.append((name, 'min', small))
        elif normal > small and normal > large:
            result.append((name, 'mid', normal))
        else:
            result.append((name, 'max', large))

    return result