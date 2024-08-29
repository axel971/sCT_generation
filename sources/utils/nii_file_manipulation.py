import numpy as np
import nibabel as nib

def get_nii_data(path: str,
                 img_dtype = np.float32):
    img = nib.load(path)
    data = img.get_fdata(dtype = img_dtype)

    if len(img.shape) == 4:
        return data[:, :, :, 0]

    else:
        return data

def get_nii_affine(path):
    img = nib.load(path)
    affine = img.affine

    return affine


