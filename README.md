

# Instructions to Download the Image Dataset
## Download the dataset

PYTHON_SCRIPT_PATH = "HOME_DIR/sources/data_acquisition/data_downloading.py" <br />
DATA_URL = "https://zenodo.org/records/7260705/files/Task1.zip?download=1" <br />
DATA_FILE_NAME = "task1.zip" <br />
DATA_OUTPUT_DIR = "HOME_DIR/data/raw_data"

python PYTHON_SCRIPT_PATH -url DATA_URL -data_file_name DATA_FILE_NAME -data_output_dir DATA_OUTPUT_DIR

## Unzip the downloaded image dataset

PYTHON_SCRIPT_PATH = "HOME_DIR/sources/data_acquisition/unzip_file.zip" <br />
FILE_PATH = "HOME_DIR/data/raw_dat/Task1.zip" <br />
OUTPUT_DIR = "HOME_DIR/data/raw_data"

python PYTHON_SCRIPT_PATH -file_path FILE_PATH -output_dir OUTPUT_DIR

