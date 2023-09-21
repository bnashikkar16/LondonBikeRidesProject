# Import the required libraries
import pandas as pd
import zipfile
import kaggle
import subprocess

# Download dataset from Kaggle using the Kaggle API
# Define the Kaggle command as a list of arguments
command = ["kaggle", "datasets", "download", "-d", "hmavrodiev/london-bike-sharing-dataset"]

# Run the command as an external process
try:
    subprocess.run(command, check=True)
    print("Dataset downloaded successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")

# Extract the downloaded zip file
with zipfile.ZipFile("london-bike-sharing-dataset.zip", "r") as zip_ref:
    zip_ref.extractall("london-bike-sharing-dataset")

# Read the CSV file as a pandas DataFrame
bikes = pd.read_csv("london-bike-sharing-dataset/london_merged.csv")

# Explore the data
print(bikes.info())
print(bikes.shape)
print(bikes)

# Count the unique values in the weather_code column
print(bikes.weather_code.value_counts())

# Count the unique values in the season column
print(bikes.season.value_counts())

# Specify the column names that you want to use
new_cols_dict = {
    'timestamp': 'time',
    'cnt': 'count',
    't1': 'temp_real_C',
    't2': 'temp_feels_like_C',
    'hum': 'humidity_percent',
    'wind_speed': 'wind_speed_kph',
    'weather_code': 'weather',
    'is_holiday': 'is_holiday',
    'is_weekend': 'is_weekend',
    'season': 'season'
}

# Rename the columns to the specified column names
bikes.rename(new_cols_dict, axis=1, inplace=True)

# Change the humidity values to percentage (i.e., a value between 0 and 1)
bikes.humidity_percent = bikes.humidity_percent / 100

# Create a season dictionary so that we can map the integers 0-3 to the actual written values
season_dict = {
    '0.0': 'spring',
    '1.0': 'summer',
    '2.0': 'autumn',
    '3.0': 'winter'
}

# Create a weather dictionary so that we can map the integers to the actual written values
weather_dict = {
    '1.0': 'Clear',
    '2.0': 'Scattered clouds',
    '3.0': 'Broken clouds',
    '4.0': 'Cloudy',
    '7.0': 'Rain',
    '10.0': 'Rain with thunderstorm',
    '26.0': 'Snowfall'
}

# Change the seasons column data type to string
bikes.season = bikes.season.astype('str')
# Map the values 0-3 to the actual written seasons
bikes.season = bikes.season.map(season_dict)

# Change the weather column data type to string
bikes.weather = bikes.weather.astype('str')
# Map the values to the actual written weathers
bikes.weather = bikes.weather.map(weather_dict)

# Check the DataFrame to see if the mappings have worked
print(bikes.head())

# Write the final DataFrame to an Excel file for Tableau visualizations
bikes.to_excel('london_bikes_final.xlsx', sheet_name='Data')