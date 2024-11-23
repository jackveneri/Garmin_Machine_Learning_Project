import ast

import numpy as np
import pandas as pd


def replace_none_with_mean(values):
    # Filter out None values and calculate the mean of the remaining values
    valid_values = [v for v in values if v is not None]
    if not valid_values:  # Check to avoid division by zero
        return values  # Return the original list if all values are None
    
    mean_value = np.mean(valid_values)
    
    # Replace None with the mean value
    return [v if v is not None else mean_value for v in values]


# Load JSON file into a DataFrame
df = pd.read_csv(r'C:\\Users\giaco\python_scripts\Garmin_Machine_Learning_Project\Garmin_Data.csv')

# Display the DataFrame
print(df.columns)
df['speed'] = df['speed'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# Apply np.max on each list
df['maxSpeed'] = df['speed'].apply(lambda x: np.max(x) if isinstance(x, list) and len(x) > 0 else np.nan)
print(df['maxSpeed'])
df['altitude'] = df['altitude'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
df['altitude'] = df['altitude'].apply(lambda x: replace_none_with_mean(x))
print(df['altitude'])
df[['elapsedDuration','heartRate','distance','lightSleep','deepSleep','apparentTemp', 'relativeHumidity', 'windSpeed']] = df[['elapsedDuration','heartRate','distance','deepSleep','lightSleep','apparentTemp', 'relativeHumidity', 'windSpeed']].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
print(df['relativeHumidity'])
# Assuming your column name is 'column_name'
#df['lightSleep'] = df['lightSleep'].apply(
#    lambda x: float(x.split()[1]) if isinstance(x, str) and x.lower() != "0 none" else None
#)
# Extract number if string is in the format "0 <number>\<string>"
if isinstance(df.loc[df.shape[0]-2,'lightSleep'],float):
    pass
else:
    df['lightSleep'] = df['lightSleep'].apply(lambda x: float(x.split()[1].split('\\')[0]) if isinstance(x, str) and x.split()[1] != 'None' else None)
    df['deepSleep'] = df['deepSleep'].apply(lambda x: float(x.split()[1].split('\\')[0]) if isinstance(x, str) and x.split()[1] != 'None' else None)

print(df['lightSleep'])
print(df['relativeHumidity'].mean())

mean_value_light_sleep = df['lightSleep'].mean()
df['lightSleep_feature'] = df['lightSleep'].fillna(mean_value_light_sleep)

mean_value_deep_sleep = df['deepSleep'].mean()
df['deepSleep_feature'] = df['deepSleep'].fillna(mean_value_deep_sleep)

print(df['deepSleep_feature'])

df.to_csv('C:/Users/giaco/python_scripts/Garmin_Machine_Learning_Project/Garmin_Data.csv',
           index=True)

print(df.head())