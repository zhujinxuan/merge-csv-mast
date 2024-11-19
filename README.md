
# Merge CSV Script

This project contains a Python script to merge multiple CSV files based on a timestamp column. The configuration is flexible, allowing different timestamp formats, and uses Pixi for dependency management.

## Project Structure
- **config.yaml**: Configuration file containing settings like input/output paths, lines to skip, and timestamp column.
- **main.py**: Python script to merge CSV files.
- **requirements.txt**: List of required Python packages.
- **pixi.toml**: Pixi configuration for project setup.

## Configuration File (`config.yaml`)
Specify the following settings:
- `input_folder`: Path to the folder containing input CSV files.
- `output_file`: Path to save the merged CSV file.
- `lines_to_skip`: Number of lines to skip in each CSV file.
- `timestamp_column`: Name of the timestamp column in the merged CSV.
- `timestamp_format`: Format of the timestamp if using a single timestamp column.
- `date_column` and `time_column`: If date and time are separate, specify their column names.
- `date_format` and `time_format`: Formats for the date and time columns.

## Running the Project
1. **Install Pixi**: Install Pixi with:
   ```sh
   curl -sSL https://install.pixi.rs | sh
   ```

2. **Install Dependencies**: Set up the Python environment and dependencies using:
   ```sh
   pixi install
   ```

3. **Run the Script**: Run the script with the configuration file:
   ```sh
   pixi run python main.py path/to/your/config.yaml
   ```

## Notes
- The script checks for conflicting timestamps and notifies if duplicates are found.
- The timestamp column will be moved to the first position in the merged output.
