import pandas as pd
import re

df = pd.read_csv("C:/Users/User/OneDrive/Desktop/AI/AI_Usage_and_Impact_on_Students_and_Professionals.csv")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

print(df.head())
print(df.info())

missing = df.isnull().sum()
missing_df = pd.DataFrame({'Пропущено': missing})
print(missing_df[missing_df['Пропущено'] > 0])
print("Всего пропущенных значений:", df.isnull().sum().sum())

def clean(x):
    if pd.isna(x):
        return x
    x = str(x).replace('$', '').replace(',', '')
    x = re.sub(r'[^0-9.\-]', '', x)
    try:
        return float(x)
    except:
        return float('nan')

cols_to_clean = ['Age', 'Monthly_Income', 'AI_Usage_Hours_Per_Day',
                 'Time_Saved_Hours_Per_Week', 'Work_or_Study_Hours_Per_Day',
                 'Monthly_AI_Cost']

for col in cols_to_clean:
    df[col] = df[col].astype(object).apply(clean)

print("\n=== ТИПЫ ПОСЛЕ ОЧИСТКИ ===")
print(df[cols_to_clean].dtypes)

num_cols = df.select_dtypes(include='number').columns
cat_cols = df.select_dtypes(include='str').columns

df[num_cols] = df[num_cols].fillna(df[num_cols].median())
df[cat_cols] = df[cat_cols].fillna(df[cat_cols].mode().iloc[0])

df[num_cols] = (df[num_cols] - df[num_cols].min()) / (df[num_cols].max() - df[num_cols].min())

print("Мин и макс после нормализации:")
print(df[num_cols].agg(['min', 'max']))

for col in cat_cols:
    if col in ['User_ID', 'Tasks_Performed']:
        continue
    counts = df[col].value_counts()
    rare = counts[counts < 10].index
    df[col] = df[col].replace(rare, 'Other')

cat_to_encode = []
for c in cat_cols:
    if c not in ['User_ID', 'Tasks_Performed']:
        cat_to_encode.append(c)
df = pd.get_dummies(df, columns=cat_to_encode, drop_first=True, dtype=int)
print(df.head())