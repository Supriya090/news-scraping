import pandas as pd

df1 = pd.DataFrame(
    {'District': ['Kathmandu', 'Dhanusa', 'Kavrepalanchowk'], 'KPI_1': [.8, .85, .75]})
df2 = pd.DataFrame(
    {'District': ['Kathmandu', 'Kavrepalanchowk', 'Dhanusa'], 'KPI_2': [.35, .65, .6]})

mergedDf = pd.merge(df1, df2, how="outer")
print(mergedDf)
