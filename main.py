import os
import pandas as pd
import yaml
import logging
from typing import List, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load configuration
def load_config(file_path: str) -> Tuple[dict, str]:
    """
    Load configuration from YAML file and return the config dict and config directory.
    
    Args:
        file_path: Path to the configuration file
        
    Returns:
        Tuple containing the configuration dictionary and the directory of the config file
    """
    with open(file_path, 'r') as file:
        config: dict = yaml.safe_load(file)
    
    # Get the directory of the config file
    config_dir: str = os.path.dirname(os.path.abspath(file_path))
    
    return config, config_dir

# Load configuration from command line argument
import sys

if len(sys.argv) < 2:
    logger.error("Please provide the path to the configuration file as an argument")
    sys.exit(1)

config_path: str = sys.argv[1]
config, config_dir = load_config(config_path)

# Convert relative paths to absolute paths if they are not already absolute
input_folder: str = config['input_folder']
output_file: str = config['output_file']

if not os.path.isabs(input_folder):
    input_folder = os.path.normpath(os.path.join(config_dir, input_folder))
    
if not os.path.isabs(output_file):
    output_file = os.path.normpath(os.path.join(config_dir, output_file))

# Log the paths
logger.info(f"Input folder: {input_folder}")
logger.info(f"Output file: {output_file}")

# Get other configuration parameters
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

# Check if input folder exists
if not os.path.exists(input_folder):
    logger.error(f"Input folder does not exist: {input_folder}")
    sys.exit(1)

csv_files: List[str] = get_csv_files(input_folder)

if not csv_files:
    logger.warning(f"No CSV files found in {input_folder}")
    sys.exit(0)

logger.info(f"Found {len(csv_files)} CSV files to process")

# Ensure output directory exists
output_dir = os.path.dirname(output_file)
if not os.path.exists(output_dir):
    logger.info(f"Creating output directory: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)

dataframes: List[pd.DataFrame] = []
for file in csv_files:
    logger.info(f"Processing file: {file}")
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
        logger.error(f"CSV file {file} does not have the necessary date/time or timestamp columns.")
        raise ValueError("CSV file does not have the necessary date/time or timestamp columns.")
    
    dataframes.append(df)

# Merge all dataframes into one and sort by timestamp
def merge_and_sort_dataframes(dataframes: List[pd.DataFrame], sort_column: str) -> pd.DataFrame:
    merged_df: pd.DataFrame = pd.concat(dataframes)
    merged_df.sort_values(by=sort_column, inplace=True)
    return merged_df

merged_df: pd.DataFrame = merge_and_sort_dataframes(dataframes, timestamp_column)
logger.info(f"Merged {len(dataframes)} dataframes with {len(merged_df)} total rows")

# Check for timestamp conflicts
def check_duplicates(df: pd.DataFrame, column: str) -> None:
    duplicates: pd.DataFrame = df[df.duplicated(subset=column, keep=False)]
    if not duplicates.empty:
        logger.warning(f"Found {len(duplicates)} rows with conflicting timestamps")
        logger.warning(duplicates[[column]])

check_duplicates(merged_df, timestamp_column)

# Save the merged dataframe to the output file
def save_dataframe_to_csv(df: pd.DataFrame, file_path: str) -> None:
    # Move the timestamp column to the first position if it is not
    if df.columns[0] != timestamp_column:
        columns = [timestamp_column] + [col for col in df.columns if col != timestamp_column]
        df = df[columns]
    df.to_csv(file_path, index=False)
    logger.info(f"Saved merged data to {file_path}")

save_dataframe_to_csv(merged_df, output_file)
logger.info("Process completed successfully")
