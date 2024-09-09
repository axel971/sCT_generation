

# Instructions to Download the Image Dataset
## Download the dataset

PYTHON_SCRIPT_PATH = "HOME_DIR/sources/data_acquisition/data_downloading.py" <br />
DATA_URL = "https://zenodo.org/records/7260705/files/Task1.zip?download=1" <br />
DATA_FILE_NAME = "task1.zip" <br />
DATA_OUTPUT_DIR = "HOME_DIR/data/raw_data"

python PYTHON_SCRIPT_PATH -url DATA_URL -data_file_name DATA_FILE_NAME -data_output_dir DATA_OUTPUT_DIR

## Unzip the downloaded image dataset

PYTHON_SCRIPT_PATH = "HOME_DIR/sources/data_acquisition/unzip_file.zip" <br />
ZIPPED_DATA_PATH = "HOME_DIR/data/raw_data/Task1.zip" <br />
UNZIPPED_DATA_DIR = "HOME_DIR/data/raw_data"

python PYTHON_SCRIPT_PATH -file_path ZIPPED_DATA_PATH -output_dir UNZIPPED_DATA_DIR

## Get the patients list

PYTHON_SCRIPT_PATH = "HOME_DIR/sources/data_acquisition/get_patients_list.py" <br />
DATA_DIR = "HOME_DIR/data/raw_data/Task1/pelvis" <br />
PATIENTS_LIST_PATH = "HOME_DIR/data/patients_list.xlsx"

python PYTHON_SCRIPT_PATH -data_dir DATA_DIR -patient_list_path PATIENTS_LIST_PATH

## Reorganize the data folders
PYTHON_SCRIPT_PATH = "HOME_DIR/sources/data_acquisition/reorganize_data_folders.py" <br />
REORGANIZE_DATA_DIR = "HOME_DIR/data/raw_data/pelvis"

python PYTHON_SCRIPT_PATH -original_data_dir DATA_DIR -reorganize_data_dir REORGANIZE_DATA_DIR -patients_list_path PATIENTS_LIST_PATH

# Preprocessing of the data

