

# Instructions to Download the Image Dataset
## Download the dataset

PYTHON_SCRIPT_PATH = "HOME_DIR/sources/data_acquisition/data_downloading.py" <br />
DATA_URL = "https://zenodo.org/records/7260705/files/Task1.zip?download=1" <br />
DATA_FILE_NAME = "Task1.zip" <br />
DATA_DIR = "HOME_DIR/data/raw_data"

python PYTHON_SCRIPT_PATH -url DATA_URL -data_file_name DATA_FILE_NAME -data_dir DATA_DIR

## Unzip the downloaded image dataset

PYTHON_SCRIPT_PATH = "HOME_DIR/sources/data_acquisition/unzip_file.zip" 

python PYTHON_SCRIPT_PATH -zipped_file_path DATA_DIR/DATA_FILE_NAME -unzipped_file_dir DATA_DIR

## Get the patients list

PYTHON_SCRIPT_PATH = "HOME_DIR/sources/data_acquisition/get_patients_list.py" <br />
PATIENTS_LIST_PATH = "HOME_DIR/data/patients_list.xlsx"

python PYTHON_SCRIPT_PATH -data_dir DATA_DIR/Task1/pelvis -patient_list_path PATIENTS_LIST_PATH

## Reorganize the data folders
PYTHON_SCRIPT_PATH = "HOME_DIR/sources/data_acquisition/reorganize_data_folders.py" <br />
REORGANIZE_DATA_DIR = "HOME_DIR/data/raw_data/pelvis"

python PYTHON_SCRIPT_PATH -original_data_dir DATA_DIR/Task1/pelvis -reorganize_data_dir REORGANIZE_DATA_DIR -patients_list_path PATIENTS_LIST_PATH

# Instructions to preprocess the data

## Compile the cxx executables
cd HOME_DIR/sources/preprocessing/lib/n4_bias_field_correction <br />
cmake . -G "MinGW Makefiles" -D CMAKE_C_COMPILER=gcc -D CMAKE_CXX_COMPILER=g++ -Bbuild -DITK_DIR="PATH_TOWARD/itk/bin/CMakeFiles" <br />
cd build <br />
mingw32-make

cd HOME_DIR/sources/preprocessing/lib/resampling<br />
cmake . -G "MinGW Makefiles" -D CMAKE_C_COMPILER=gcc -D CMAKE_CXX_COMPILER=g++ -Bbuild -DITK_DIR="PATH_TOWARD/itk/bin/CMakeFiles"<br />
cd build <br />
mingw32-make

## Run the preprocessing script

PYTHON_SCRIPT_PATH = HOME_DIR/sources/preprocessing/preprocessing.py <br />
PREPROCESSED_DATA_DIR = HOME_DIR/data/preprocessing/pelvis

python PYTHON_SCRIPT_PATH -output_dir PREPROCESSED_DATA_DIR -CT_dir DATA_DIR/pelvis/CT -MRI_dir DATA_DIR/pelvis/MRI -mask_dir DATA_DIR/pelvis/mask -patients_list_path PATIENTS_LIST_PATH -img_ext ".nii.gz" -resampling_cxx HOME_DIR/sources/preprocessing/lib/resampling/build/bin/resampling.exe -bias_field_correction_cxx HOME_DIR/sources/preprocessing/lib/n4_bias_field_correction/build/bin/n4_bias_field_correction.exe

# Instructions to train the deep learning models

PYTHON_SCRIPT_PATH = HOME_DIR/sources/main/main_UNet_2d.py <br />
PREDICTED_DATA_DIR = HOME_DIR/data/predictions/

python PYTHON_SCRIPT_PATH -patients_list_path PATIENTS_LIST_PATH -mri_dir PREPROCESSED_DATA_DIR/MRI/bias_field_correction -ct_dir PREPROCESSED_DATA_DIR/CT/resampling -sct_dir PREDICTED_DATA_DIR/UNet_2d" -img_ext ".nii.gz"


