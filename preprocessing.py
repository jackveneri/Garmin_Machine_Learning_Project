import pandas as pd

df = pd.read_csv(r'C:\\Users\giaco\python_scripts\Garmin_Machine_Learning_Project\Garmin_Data.csv')
print(df.loc[0,'speed'])
