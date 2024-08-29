import numpy as np
import SimpleITK as sitk

def get_image(path: str):
    
    image = sitk.ReadImage(path)

    return sitk.GetArrayFromImage(image)
        
def get_data(path: str):
    
    image = sitk.ReadImage(path)

    return sitk.GetArrayFromImage(image), image.GetOrigin(), image.GetSpacing(), image.GetDirection()

def save_image(image_array: np.float32,
               path: str,
               origin,
               spacing,
               direction
               ):
    
    image = sitk.GetImageFromArray(image_array)
    image.SetOrigin(origin)
    image.SetSpacing(spacing)
    image.SetDirection(direction)

    sitk.WriteImage(image, path)
    
