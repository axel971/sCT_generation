
# -output_dir = "C:\Users\axell\Documents\dev\sCT_generation\data\preprocessing\pelvis"
# -CT_dir = "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\pelvis\CT"
# -MRI_dir = "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\pelvis\MRI"
# -mask_dir = "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\pelvis\mask"
# -patients_list_path = "C:\Users\axell\Documents\dev\sCT_generation\data\patients_list.xlsx"
# -img_ext = ".nii.gz"
# -resampling_cxx = C:\Users\axell\Documents\dev\sCT_generation\sources\preprocessing\lib\resampling\build\bin\resampling.exe
# -bias_field_correction_cxx = C:\Users\axell\Documents\dev\sCT_generation\sources\preprocessing\lib\n4_bias_field_correction\build\bin\n4_bias_field_correction.exe

# python preprocessing.py -output_dir "C:\Users\axell\Documents\dev\sCT_generation\data\preprocessing\pelvis" -CT_dir "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\pelvis\CT" -MRI_dir "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\pelvis\MRI" -mask_dir "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\pelvis\mask" -patients_list_path "C:\Users\axell\Documents\dev\sCT_generation\data\patients_list.xlsx" -img_ext ".nii.gz" -resampling_cxx C:\Users\axell\Documents\dev\sCT_generation\sources\preprocessing\lib\resampling\build\bin\resampling.exe -bias_field_correction_cxx  C:\Users\axell\Documents\dev\sCT_generation\sources\preprocessing\lib\n4_bias_field_correction\build\bin\n4_bias_field_correction.exe
#

import argparse
from pathlib import Path
import pandas as pd
import subprocess

def main(output_dir: str,
         CT_dir: str,
         MRI_dir: str,
         mask_dir: str,
         patients_list_path: str,
         img_ext: str,
         resampling_cxx: str,
         bias_field_correction_cxx: str):


    OUTPUT_DIR = Path(output_dir)
    CT_DIR = Path(CT_dir)
    MRI_DIR = Path(MRI_dir)
    MASK_DIR = Path(mask_dir)
    PATIENTS_LIST_PATH = Path(patients_list_path)

    # Create the output folders that will contain all the preprocessed images
    OUTPUT_DIR.mkdir(parents = True, exist_ok = True)

    OUTPUT_CT_DIR = OUTPUT_DIR / "CT"
    OUTPUT_CT_DIR.mkdir(parents = True, exist_ok = True)
    
    OUTPUT_MRI_DIR = OUTPUT_DIR / "MRI"
    OUTPUT_MRI_DIR.mkdir(parents = True, exist_ok = True)

    OUTPUT_MASK_DIR = OUTPUT_DIR / "mask"
    OUTPUT_MASK_DIR.mkdir(parents = True, exist_ok = True)

    ### Resampling
    OUTPUT_RESAMPLED_CT_DIR = OUTPUT_CT_DIR / "resampling"
    OUTPUT_RESAMPLED_CT_DIR.mkdir(parents = True, exist_ok = True)

    OUTPUT_RESAMPLED_MRI_DIR = OUTPUT_MRI_DIR / "resampling"
    OUTPUT_RESAMPLED_MRI_DIR.mkdir(parents = True, exist_ok = True)

    OUTPUT_RESAMPLED_MASK_DIR = OUTPUT_MASK_DIR / "resampling"
    OUTPUT_RESAMPLED_MASK_DIR.mkdir(parents = True, exist_ok = True)

    ### Bias field corection: N4 algorithm
    OUTPUT_BIAS_FIELD_CORRECTED_MRI_DIR = OUTPUT_MRI_DIR / "bias_field_correction"
    OUTPUT_BIAS_FIELD_CORRECTED_MRI_DIR.mkdir(parents = True, exist_ok = True)

    # Get the patient list 
    patients_list = pd.read_excel(PATIENTS_LIST_PATH, header = 0, index_col = 0)["patient_name"]
    

    # Start preprocessing
    for patient in patients_list:
        
        print(f"*** start preprocessing of patient: {patient} **** ")

        # Resampling
        print(f"*Resampling")
        
        subprocess.run([resampling_cxx, CT_DIR / (patient + img_ext), OUTPUT_RESAMPLED_CT_DIR / (patient + img_ext),"256", "256", "128" ])
        print("CT done ...")

        subprocess.run([resampling_cxx, MRI_DIR / (patient + img_ext), OUTPUT_RESAMPLED_MRI_DIR / (patient + img_ext),"256", "256", "128" ])
        print("MRI done ...")

        subprocess.run([resampling_cxx, MASK_DIR / (patient + img_ext), OUTPUT_RESAMPLED_MASK_DIR / (patient + img_ext),"256", "256", "128" ])
        print("Mask done ...")

        # Bias field corection
        print("*Bias field corection")

        subprocess.run([bias_field_correction_cxx, OUTPUT_RESAMPLED_MRI_DIR / (patient + img_ext), OUTPUT_RESAMPLED_MASK_DIR / (patient + img_ext), OUTPUT_BIAS_FIELD_CORRECTED_MRI_DIR / (patient + img_ext)])
        print("MRI done ...")

    return



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "Python script for running all preprocessing processes")
    parser.add_argument("-output_dir", required = True, help = "Path toward the directory that will contain all processed data")
    parser.add_argument("-CT_dir", required = True, help = "Path toward the raw CT images")
    parser.add_argument("-MRI_dir", required = True, help = "Path toward the raw MR images")
    parser.add_argument("-mask_dir", required = True, help = "Path toward the raw mask images")
    parser.add_argument("-patients_list_path", required = True, help = "Path toward the Excel patients list file")
    parser.add_argument("-img_ext", required = True, help = "image extension")
    parser.add_argument("-resampling_cxx", required = True, help = "Path toward the C++ executable doing the resampling")
    parser.add_argument("-bias_field_correction_cxx", required = True, help = "Path toward the bias field correction C++ executable")
    args = parser.parse_args()

    main(output_dir = args.output_dir,
         CT_dir = args.CT_dir,
         MRI_dir = args.MRI_dir,
         mask_dir = args.mask_dir,
         patients_list_path = args.patients_list_path,
         img_ext = args.img_ext,
         resampling_cxx = args.resampling_cxx,
         bias_field_correction_cxx = args.bias_field_correction_cxx
         )
