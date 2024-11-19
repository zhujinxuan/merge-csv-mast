
import os
import pandas as pd
import yaml
from typing import List, Optional

# Load configuration
def load_config(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        config: dict = yaml.safe_load(file)
    return config

# Load configuration
import sys

# Load configuration from command line argument
config_path: str = sys.argv[1]
config: dict = load_config(config_path)

input_folder: str = config['input_folder']
output_file: str = config['output_file']
lines_to_skip: int = config['lines_to_skip']
timestamp_column: str = config['timestamp_column']
timestamp_format: Optional[str] = config.get('timestamp_format')
date_column: Optional[str] = config.get('date_column')
date_format: Optional[str] = config.get('date_format')
time_column: Optional[str] = config.get('time_column')
time_format: Optional[str] = config.get('time_format')

# Read all CSV files in the input folder
def get_csv_files(folder_path: str) -> List[str]:
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]

csv_files: List[str] = get_csv_files(input_folder)

dataframes: List[pd.DataFrame] = []
for file in csv_files:
    df: pd.DataFrame = pd.read_csv(file, skiprows=lines_to_skip)
    
    # If both date and time columns are present, combine them into a timestamp column
    if date_column in df.columns and time_column in df.columns:
        df[timestamp_column] = pd.to_datetime(
            df[date_column] + ' ' + df[time_column], 
            format=f"{date_format} {time_format}"
        ).dt.strftime(timestamp_format)
        df.drop(columns=[date_column, time_column], inplace=True)
    elif timestamp_column in df.columns and timestamp_format:
        df[timestamp_column] = pd.to_datetime(df[timestamp_column], format=timestamp_format).dt.strftime(timestamp_format)
    else:
        raise ValueError("CSV file does not have the necessary date/time or timestamp columns.")
    
    dataframes.append(df)

# Merge all dataframes into one and sort by timestamp
def merge_and_sort_dataframes(dataframes: List[pd.DataFrame], sort_column: str) -> pd.DataFrame:
    merged_df: pd.DataFrame = pd.concat(dataframes)
    merged_df.sort_values(by=sort_column, inplace=True)
    return merged_df

merged_df: pd.DataFrame = merge_and_sort_dataframes(dataframes, timestamp_column)

# Check for timestamp conflicts
def check_duplicates(df: pd.DataFrame, column: str) -> None:
    duplicates: pd.DataFrame = df[df.duplicated(subset=column, keep=False)]
    if not duplicates.empty:
        print("Conflicting timestamps found:")
        print(duplicates[[column]])

check_duplicates(merged_df, timestamp_column)

# Save the merged dataframe to the output file
def save_dataframe_to_csv(df: pd.DataFrame, file_path: str) -> None:
    # Move the timestamp column to the first position if it is not
    if df.columns[0] != timestamp_column:
        columns = [timestamp_column] + [col for col in df.columns if col != timestamp_column]
        df = df[columns]
    df.to_csv(file_path, index=False)

save_dataframe_to_csv(merged_df, output_file)
