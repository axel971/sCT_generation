from pathlib import Path
import numpy as np
import torch
import torchmetrics

def predict(model: torch.nn.Module,
         dataloader: torch.utils.data.DataLoader,
         device):

    test_pred = []

    model.eval()
    with torch.inference_mode():
        for x in dataloader:
  
            x = x[0].to(device)
            test_pred.append(model(x))

            
    return torch.cat(test_pred, dim = 0)
