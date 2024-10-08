# -patients_list_path = "C:\Users\axell\Documents\dev\sCT_generation\data\patients_list.xlsx" 
# -mri_dir = C:\Users\axell\Documents\dev\sCT_generation\data\preprocessing\pelvis\MRI\bias_field_correction
# -ct_dir = C:\Users\axell\Documents\dev\sCT_generation\data\preprocessing\pelvis\CT\resampling
# -sct_dir = C:\Users\axell\Documents\dev\sCT_generation\data\predictions\UNet_2d
# -img_ext = ".nii.gz"
#
# python main_UNet_2d.py -patients_list_path "C:\Users\axell\Documents\dev\sCT_generation\data\patients_list.xlsx" -mri_dir C:\Users\axell\Documents\dev\sCT_generation\data\preprocessing\pelvis\MRI\bias_field_correction -ct_dir C:\Users\axell\Documents\dev\sCT_generation\data\preprocessing\pelvis\CT\resampling -sct_dir "C:\Users\axell\Documents\dev\sCT_generation\data\predictions\pelvis\UNet_2d" -img_ext ".nii.gz"
#

from pathlib import Path
import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import TensorDataset, DataLoader
from torchmetrics.regression import MeanAbsoluteError
import time
import sys

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from utils.nii_file_manipulation import get_nii_data
from models.UNet_2d import UNet_2d
from models.training_functions import train
from models.testing_functions import predict
from utils.simpleITK_utils import get_image, get_data, save_image
import evaluation.metrics as metrics

def main(patients_list_path: str,
         mri_dir: str,
         ct_dir: str,
         sct_dir: str,
         img_ext: str):

    patients_list = pd.read_excel(patients_list_path, header = 0, index_col = 0)["patient_name"].to_numpy()
    #patients_list = patients_list[0:3]

    print("*** Load the images ***")
    start_time = time.time()

    MRI_DIR = Path(mri_dir)
    CT_DIR = Path(ct_dir)
    
    mris = []
    cts = []
    origins = []
    spacings = []
    directions = []

    for patient in patients_list:
        mri, origin, spacing, direction = get_data(MRI_DIR / (patient + img_ext))
        mris.append(mri)
        origins.append(origin)
        spacings.append(spacing)
        directions.append(direction)
        cts.append(get_image(CT_DIR / (patient + img_ext)))

    end_time = time.time()
    print(f"Done ... execution time: {end_time - start_time}")

    print("*** Separate the images in training/testing datasets ***")
    
    training_mris, testing_mris, training_cts, testing_cts, training_patients_list, testing_patients_list = train_test_split(mris, cts,patients_list, test_size = 0.30, random_state = 42)

    print("Done ...")

    print("*** Extract slices from images ***") # NB: Part to improve (look for memory efficiency and code simplicity)
    start_time = time.time()

    training_mri_slices = []
    training_ct_slices = []

    for iPatient in range(len(training_patients_list)):
        for iSlice in range(training_mris[0].shape[0]):

            training_mri_slices.append(training_mris[iPatient][iSlice, :, :])
            training_ct_slices.append(training_cts[iPatient][iSlice, :, :])

    end_time = time.time()
    print(f"Done ... execution time: {end_time - start_time}")

    print("*** Convert your training mri and ct slices into pytorch dataset ***")
    start_time = time.time()

    training_dataset = TensorDataset(torch.from_numpy(np.array(training_mri_slices)).unsqueeze(1),
                                     torch.from_numpy(np.array(training_ct_slices)).unsqueeze(1))
    

    end_time = time.time()
    print(f"Done ... execution time: {end_time - start_time}")
    
    print("*** Start training ***")
    start_time = time.time()

    TRAINING_BATCH_SIZE = 16
    EPOCHS = 2
    training_dataloader = DataLoader(training_dataset,
                                     batch_size = TRAINING_BATCH_SIZE,
                                     shuffle = True)

    device = "gpu" if torch.cuda.is_available() else "cpu" # design device agnostic code

    model = UNet_2d(1, 1).to(device)
    
    loss_fn = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(params = model.parameters(), lr = 0.01)
    metric_fn = MeanAbsoluteError()
    
    
    model_result = train(model = model,
                         dataloader = training_dataloader,
                         optimizer = optimizer,
                         loss_fn = loss_fn,
                         metric_fn = metric_fn,
                         epochs = EPOCHS,
                         device = device)
    
    
    end_time = time.time()
    print("Done ...")
    
    print("*** Start testing ***")
    start_time = time.time()

    SCT_DIR = Path(sct_dir)
    SCT_DIR.mkdir(parents = True, exist_ok = True)

    TESTING_BATCH_SIZE = 16
    maes = []

    for iPatient in range(len(testing_patients_list)):

        iPatient_testing_mri_slices = testing_mris[iPatient]

        iPatient_testing_dataset = TensorDataset(torch.from_numpy(iPatient_testing_mri_slices).unsqueeze(dim = 1))
        iPatient_testing_dataloader = DataLoader(iPatient_testing_dataset,
                                         batch_size = TESTING_BATCH_SIZE)
     
        iPatient_prediction = predict(model = model,
                                   dataloader = iPatient_testing_dataloader,
                                   device = device)

        sct = iPatient_prediction.squeeze(dim = 1).numpy()
        
        # Evaluate model performance
        maes.append(metrics.mae(sct, testing_cts[iPatient]))
       
        # Save sCT image
        save_image(iPatient_prediction.squeeze(dim = 1).numpy(),
                   SCT_DIR / (testing_patients_list[iPatient] + img_ext),
                   origins[iPatient],
                   spacings[iPatient],
                   directions[iPatient])
        
    
    end_time = time.time()
    print(f"done ... exectution time: {end_time - start_time}")

    print("*** Model performance on testing dataset ***")
    print(f"MAE: {np.mean(np.array(maes))}")

    return


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "Train and evaluate U-Net for sCT generation")
    parser.add_argument("-patients_list_path", required = True, help = "Path toward the excel file containing the patients name")
    parser.add_argument("-mri_dir", required = True, help = "Path toward the MR image directory")
    parser.add_argument("-ct_dir", required = True, help = "Path toward the CT image directory")
    parser.add_argument("-sct_dir", required = True, help = "Path toward the predicted sCT image directory")
    parser.add_argument("-img_ext", required = True, help = "Extension of the image files")
    args = parser.parse_args()

    main(patients_list_path = args.patients_list_path,
         mri_dir = args.mri_dir,
         ct_dir = args.ct_dir,
         sct_dir = args.sct_dir,
         img_ext = args.img_ext)

