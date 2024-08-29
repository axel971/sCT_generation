import os
from pathlib import Path
import argparse
import pandas as pd

# dir = "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\Task1\pelvis"
# output_list_path = "C:\Users\axell\Documents\dev\sCT_generation\data\patient_names.xlsx"
# python get_patients_list.py -dir "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\Task1\pelvis" -output_list_path C:\Users\axell\Documents\dev\sCT_generation\data\patients_list.xlsx

def main(directory: str, output_list_path: str):

    DIR = Path(directory)
    OUTPUT_LIST_PATH = Path(output_list_path)
    patients_list = []

    for path in DIR.iterdir(): # Get subdirectories path
        if path.name != "overview":
            patients_list.append(path.name)
            print (path.name)

    df = pd.DataFrame(patients_list, columns = ["patient_name"])
    df.to_excel(OUTPUT_LIST_PATH)

    return


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "Get a list of patient names")
    parser.add_argument("-dir", metavar = "string", required = True, help = "Path of the directory containing subdirectories with patient names")
    parser.add_argument("-output_list_path", metavar = "string", required = True, help = "Path of the obtained patient names' list")
    args = parser.parse_args()

    main(directory = args.dir, output_list_path = args.output_list_path)


