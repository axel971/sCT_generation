import os
from pathlib import Path
import argparse
import pandas as pd

# data_dir = "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\Task1\pelvis"
# patients_list_path = "C:\Users\axell\Documents\dev\sCT_generation\data\patients_list.xlsx"
# python get_patients_list.py -data_dir "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\Task1\pelvis" -patients_list_path C:\Users\axell\Documents\dev\sCT_generation\data\patients_list.xlsx

def main(data_dir: str, patients_list_path: str):

    DATA_DIR = Path(data_dir)
    PATIENTS_LIST_PATH = Path(patients_list_path)
    patients_list = []

    for path in DATA_DIR.iterdir(): # Get subdirectories path
        if path.name != "overview":
            patients_list.append(path.name)
            print (path.name)

    df = pd.DataFrame(patients_list, columns = ["patient_name"])
    df.to_excel(PATIENTS_LIST_PATH)

    return


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "Get a list of patient names")
    parser.add_argument("-data_dir", metavar = "string", required = True, help = "Path toward the directory containing subdirectories named with patient IDs")
    parser.add_argument("-patients_list_path", metavar = "string", required = True, help = "Path of the patient list file")
    args = parser.parse_args()

    main(data_dir = args.data_dir, patients_list_path = args.patients_list_path)


