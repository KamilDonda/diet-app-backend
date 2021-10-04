import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

def load_data_pandas():
    data = pd.read_csv('data.csv', engine='python')
    data = data.drop(columns=[])
    return data

df = load_data_pandas()
# df = df[df['Serving Size'].str.contains(' g')]
# df['Serving Size'] = df['Serving Size'].str.replace(')','').str.replace(' g','').str.split('(').str[1]

print(df)

# df.to_csv('data.csv', index=False)