import pandas as pd
from thefuzz import fuzz


df1 = pd.DataFrame(
    {'District': ['Kathmandu', 'Dhanusa', 'Kavrepalanchowk'], 'KPI_1': [.8, .85, .75]})
df2 = pd.DataFrame(
    {'District': ['Kathmandu', 'Kavre palanchowk', 'Dhanusha'], 'KPI_2': [.35, .65, .6]})

# creates a new dataframe after sorting
df1_sorted = df1.sort_values(by='District', inplace=False).reset_index()
df2_sorted = df2.sort_values(by='District', inplace=False).reset_index()

# renames the dataframe if the fuzz similarity is greater than 90
for i in range(df1.shape[0]):
    if (fuzz.ratio(df1_sorted['District'][i], df2_sorted['District'][i])) > 90:
        df2_sorted['District'] = df1_sorted['District']

# merging the dataframes
mergedDf = pd.merge(df1_sorted, df2_sorted, on="District", how="outer")

print(mergedDf)
