from pathlib import Path
import argparse
import pandas as pd
import shutil

# -original_data_dir = "C:\Users\axell\iDocuments\dev\sCT_generation\data\raw_data\Task1\pelvis"
# -reorganize_data_dir = "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\pelvis"
# -patients_list_path = "C:\Users\axell\Documents\dev\sCT_generation\data\patients_list.xlsx"
# python reorganize_data_folders.py -original_data_dir "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\Task1\pelvis" -reorganize_data_dir "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\pelvis" -patients_list_path "C:\Users\axell\Documents\dev\sCT_generation\data\patients_list.xlsx"


def main(original_data_dir: str, 
         reorganize_data_dir: str,
         patients_list_path: str):
    
    ORIGINAL_DATA_DIR = Path(original_data_dir)
    REORGANIZE_DATA_DIR = Path(reorganize_data_dir)
    PATIENTS_LIST_PATH = Path(patients_list_path)
    OUTPUT_CT_DIR = REORGANIZE_DATA_DIR / "CT"
    OUTPUT_MRI_DIR = REORGANIZE_DATA_DIR / "MRI"
    OUTPUT_MASK_DIR = REORGANIZE_DATA_DIR / "mask"

    REORGANIZE_DATA_DIR.mkdir(parents = True, exist_ok = True)
    OUTPUT_CT_DIR.mkdir(parents = True, exist_ok = True)
    OUTPUT_MRI_DIR.mkdir(parents = True, exist_ok = True)
    OUTPUT_MASK_DIR.mkdir(parents = True, exist_ok = True)

    patients_list = pd.read_excel(PATIENTS_LIST_PATH, index_col = 0, header = 0)  

    names = patients_list["patient_name"]
    for name in names:
        
        shutil.copy(ORIGINAL_DATA_DIR / name / "ct.nii.gz", OUTPUT_CT_DIR / (name + ".nii.gz"))
        shutil.copy(ORIGINAL_DATA_DIR / name / "mr.nii.gz", OUTPUT_MRI_DIR / (name + ".nii.gz"))
        shutil.copy(ORIGINAL_DATA_DIR / name / "mask.nii.gz", OUTPUT_MASK_DIR / (name + ".nii.gz"))

    return


if __name__ == "__main__" :

    parser = argparse.ArgumentParser("Reorganize data folders")
    parser.add_argument("-original_data_dir", metavar = "string", required = True, help = "Directory containing the original files")
    parser.add_argument("-reorganize_data_dir", metavar = "string", required = True, help = "Directory containing all the new reorganized files")
    parser.add_argument("-patients_list_path", metavar = "string", required = True, help = "Path toward excel patients list")
    args = parser.parse_args()


    main(original_data_dir = args.original_data_dir, reorganize_data_dir = args.reorganize_data_dir, patients_list_path = args.patients_list_path)

