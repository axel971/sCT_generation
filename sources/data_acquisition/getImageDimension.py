import numpy as np
import pandas as pd
import argparse
from pathlib import Path
import sys

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from utils.simpleITK_utils import get_image

# img_dir = C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\pelvis\MRI
# patients_list_path = C:\Users\axell\Documents\dev\sCT_generation\data\patients_list.xlsx
# ext = ".nii.gz"
# python getImageDimension.py -img_dir "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\pelvis\MRI" -patients_list_path "C:\Users\axell\Documents\dev\sCT_generation\data\patients_list.xlsx" -ext ".nii.gz" 

def main(img_dir: str,
         patients_list_path: str,
         ext: str):

    IMG_DIR = Path(img_dir)
    PATIENTS_LIST_PATH = Path(patients_list_path)

    data = pd.read_excel(PATIENTS_LIST_PATH, header = 0, index_col = 0)
    patients_list = np.array(data.iloc[:, 0], dtype = np.str_)

    # Load images and stock their shape/dimensions in an airray
    shapes = []
    for patient in patients_list:
        shapes.append(get_image(IMG_DIR / (patient + ext)).shape)

    shapes = np.array(shapes)
    print(shapes.shape)
    print(shapes[0, 0])
    print(shapes[0, 1])
    print(shapes[0, 2])

    return

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "")
    parser.add_argument('-img_dir', metavar = "string", required = True, help = "Path toward the directory containing the images")
    parser.add_argument('-patients_list_path', metavar = "string", required = True, help = "Path toward the excel file containing the name of the images" )
    parser.add_argument('-ext', required = True, help = "File extension of the images")
    args = parser.parse_args()

    main(img_dir = args.img_dir, patients_list_path = args.patients_list_path, ext = args.ext)


