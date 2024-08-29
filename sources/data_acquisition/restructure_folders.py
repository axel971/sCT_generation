from pathlib import Path
import argparse
import pandas as pd
import shutil

# -input_dir = "C:\Users\axell\iDocuments\dev\sCT_generation\data\raw_data\Task1\pelvis"
# -output_dir = "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\pelvis"
# -patients_list_path = "C:\Users\axell\Documents\dev\sCT_generation\data\patients_list.xlsx"
# python restructure_folders.py -input_dir "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\Task1\pelvis" -output_dir "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\pelvis" -patients_list_path "C:\Users\axell\Documents\dev\sCT_generation\data\patients_list.xlsx"


def main(input_dir: str, output_dir: str, patients_list_path: str):
    
    INPUT_DIR = Path(input_dir)
    OUTPUT_DIR = Path(output_dir)
    PATIENTS_LIST_PATH = Path(patients_list_path)
    OUTPUT_CT_DIR = OUTPUT_DIR / "CT"
    OUTPUT_MRI_DIR = OUTPUT_DIR / "MRI"
    OUTPUT_MASK_DIR = OUTPUT_DIR / "mask"

    OUTPUT_DIR.mkdir(parents = True, exist_ok = True)
    OUTPUT_CT_DIR.mkdir(parents = True, exist_ok = True)
    OUTPUT_MRI_DIR.mkdir(parents = True, exist_ok = True)
    OUTPUT_MASK_DIR.mkdir(parents = True, exist_ok = True)

    patients_list = pd.read_excel(PATIENTS_LIST_PATH, index_col = 0, header = 0)  

    names = patients_list["patient_name"]
    for name in names:
        
        shutil.copy(INPUT_DIR / name / "ct.nii.gz", OUTPUT_CT_DIR / (name + ".nii.gz"))
        shutil.copy(INPUT_DIR / name / "mr.nii.gz", OUTPUT_MRI_DIR / (name + ".nii.gz"))
        shutil.copy(INPUT_DIR / name / "mask.nii.gz", OUTPUT_MASK_DIR / (name + ".nii.gz"))

    return


if __name__ == "__main__" :

    parser = argparse.ArgumentParser("Restructure folders")
    parser.add_argument("-input_dir", metavar = "string", required = True, help = "Directory containing the original files")
    parser.add_argument("-output_dir", metavar = "string", required = True, help = "Directory containing all the new restructured files")
    parser.add_argument("-patients_list_path", metavar = "string", required = True, help = "Path toward excel patients list")
    args = parser.parse_args()


    main(input_dir = args.input_dir, output_dir = args.output_dir, patients_list_path = args.patients_list_path)

