import numpy
import torch
import torchmetrics
from tqdm.auto import tqdm


def train(model: torch.nn.Module,
          dataloader: torch.utils.data.DataLoader,
          optimizer: torch.optim.Optimizer,
          loss_fn: torch.nn.Module,
          metric_fn: torchmetrics,
          epochs: int,
          device
          ):

    results = { "train_loss": [],
               "train_metric": []
            }

    for epoch in range(epochs):
        
        print(f"Epoch {epoch + 1}/{epochs}:")

        train_loss, train_metric = train_step(model,
                                              dataloader,
                                              loss_fn,
                                              optimizer,
                                              metric_fn,
                                              device)

        print(f"Epoch {epoch + 1} | Train loss: {train_loss:.4f} | Train metric: {train_metric}")

        results["train_loss"].append(train_loss)
        results["train_metric"].append(train_metric)
   
    return results


def train_step(model: torch.nn.Module,
               dataloader: torch.utils.data.DataLoader,
               loss_fn: torch.nn.Module,
               optimizer: torch.optim.Optimizer,
               metric_fn: torchmetrics,
               device):

    model.train()

    train_loss = 0
    
    loop = tqdm(dataloader)

    for (x, y) in loop:

        x, y = x.to(device), y.to(device) # Put batch on device (gpu or cpu)
               
        y_pred = model(x)
        
        # Compute the loss on current batch
        loss = loss_fn(y_pred, y)
        train_loss += loss.item()

        # Compute metric on current batch
        metric = metric_fn(y_pred, y)

        # Display loss and metric results for current batch
        loop.set_postfix(loss = loss.item() , metric = metric.item())

        # Update model weights
        optimizer.zero_grad() # Reset gradiant computation (avoid gradiant accumulation across the loop) 

        loss.backward() # Back propagation

        optimizer.step() # Gradiant descent
    

    train_loss = train_loss / len(dataloader)
    train_metric = metric_fn.compute()

    metric_fn.reset()

    return train_loss, train_metric

