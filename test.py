import pandas as pd
import ast 

# Load JSON file into a DataFrame
df = pd.read_csv(r'C:\\Users\giaco\python_scripts\Garmin_Machine_Learning_Project\Garmin_Data_sleep.csv')

# Display the DataFrame
print(df.columns)
#print(df.iloc[0])
print(df.loc[30, ['dailySleepDTO.deepSleepSeconds','dailySleepDTO.lightSleepSeconds','dailySleepDTO.calendarDate']])

df2 = pd.read_csv(r'C:\\Users\giaco\python_scripts\Garmin_Machine_Learning_Project\Garmin_Data_weather.csv')
print(df2.columns)
print(df2.loc[1, ['issueDate','apparentTemp','relativeHumidity', 'windSpeed']])
test = ast.literal_eval(df2.loc[1, 'weatherTypeDTO']).get('desc')
print(test)