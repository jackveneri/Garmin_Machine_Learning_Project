from garminconnect import Garmin
import datetime
import pandas as pd

# Update with your own credentials
username = "jackveneri@gmail.com"
password = "Giacomo99"

# Connect to the API
try:
    api = Garmin(username, password)
    api.login()
except Exception as e:
    print(f"An error occurred while initializing the API: {e}")

# Set the start and end date 
activity_start_date = datetime.date(2024, 7, 8)
activity_end_date = datetime.date(2024, 11, 4)

# Call the API and create a list of activities from that timeframe
activities = api.get_activities_by_date(
    activity_start_date.isoformat(),
    activity_end_date.isoformat(),
)

# Initialize an empty list to store the activity data
activity_data = []
activity_data_weather = []
activity_data_sleep = []

# Loop over each activity
for activity in activities:
    activity_id = activity['activityId']
    details = api.get_activity_details(activity_id)  # Get detailed activity data
    activity_details = details  # Store the detailed data
    
    weather = api.get_activity_weather(activity_id)
    activity_data_weather.append(weather)    

    current_date = activity_start_date
    while current_date <=  activity_end_date:
        sleep = api.get_sleep_data(current_date)
        activity_data_sleep.append(sleep)
        current_date += datetime.timedelta(days=1)
    # Retrieve the metric descriptors for this activity
    metric_descriptors = activity_details['metricDescriptors']
    
    # Initialize a dictionary to store the metrics for this activity
    metric_data = {descriptor['key']: [] for descriptor in metric_descriptors}

    # Get activity detail metrics
    activity_detail_metrics = activity_details['activityDetailMetrics']

    # Loop over each timestamp's data (each element in activity_detail_metrics)
    for timestamp_data in activity_detail_metrics:
        # For each metric (descriptor), append the corresponding value
        for descriptor in metric_descriptors:
            metric_name = descriptor['key']
            metrics_index = descriptor['metricsIndex']
            # Ensure to check if the index is within bounds
            if metrics_index < len(timestamp_data['metrics']):
                metric_value = timestamp_data['metrics'][metrics_index]
                metric_data[metric_name].append(metric_value)
            else:
                metric_data[metric_name].append(None)  # Padding with None if index is out of bounds

    # Extract the start date for indexing, assuming 'startTimeLocal' is available and in datetime format
    activity_date = activity.get('startTimeLocal', None)

    # Collect the activity information along with metrics
    activity_info = {
        'activityId': activity_id,
        'activity_date': activity_date,  # Use activity_date for indexing
        'heartRate': metric_data.get('directHeartRate', []),
        'distance': metric_data.get('sumDistance', []),
        'speed': metric_data.get('directSpeed', []),
        'altitude': metric_data.get('directElevation', []),
        # Add more metrics as needed
    }

    # Append the activity info to the list
    activity_data.append(activity_info)

# Convert the data to a pandas DataFrame
df = pd.DataFrame(activity_data)

# Convert the 'activity_date' to datetime if needed and set as index
df['activity_date'] = pd.to_datetime(df['activity_date'])
df.set_index('activity_date', inplace=True)

# Convert list columns to string representation (if needed)
for column in ['heartRate', 'distance', 'speed', 'altitude']:
    df[column] = df[column].apply(lambda x: str(x) if isinstance(x, list) else x)

# Print the DataFrame
print(df)

# Save the DataFrame to CSV
df.to_csv('C:/Users/giaco/python_scripts/Garmin_Machine_Learning_Project/Garmin_Data.csv', index=True)
