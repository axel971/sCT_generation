import numpy as np
import torch
import torchmetrics
from tqdm.auto import tqdm

class vanillaGAN():
    def __init__(self,
                 train_dataloader: torch.utils.data.DataLoader,
                 generator: torch.nn.Module,
                 discriminator: torch.nn.Module,
                 generator_loss_fns,
                 discriminator_loss_fn: torch.nn.Module,
                 generator_optimizer: torch.optim.Optimizer,
                 discriminator_optimizer: torch.optim.Optimizer,
                 discriminator_metric_fn: torchmetrics,
                 generator_metric_fn: torchmetrics,
                 epochs: int,
                 device
                 ):

        #super().__init__()

        self.generator = generator
        self.discriminator = discriminator
        self.train_dataloader = train_dataloader
        self.generator_loss_fns = generator_loss_fns
        self.discriminator_loss_fn = discriminator_loss_fn
        self.generator_optimizer = generator_optimizer
        self.discriminator_optimizer = discriminator_optimizer
        self.discriminator_metric_fn = discriminator_metric_fn
        self.generator_metric_fn = generator_metric_fn
        self.epochs = epochs
        self.device = device
        
    def train_step(self):

        # NB: check when to put tensor on device

        discriminator_loss_for_given_epoch = 0
        generator_loss_for_given_epoch = 0
        
        loop = tqdm(self.train_dataloader)

        torch.autograd.set_detect_anomaly(True)

        for x, y in loop:
            
            x, y = x.to(self.device), y.to(self.device)
            
            # Update discriminator weights
            self.discriminator.train()
            self.generator.eval()

            discriminator_labels = torch.cat((torch.zeros((x.shape[0], 1)), torch.ones((x.shape[0], 1))), dim = 0)
            test = self.generator(x)
            #print(torch.isnan(x).any())
            #print(torch.isnan(y).any())
            #print(torch.isnan(test).any())

            discriminator_predicted_labels = torch.cat((self.discriminator(test),
                                                        self.discriminator(y)),
                                                       dim = 0)

            discriminator_loss = self.discriminator_loss_fn(discriminator_predicted_labels, discriminator_labels)
            discriminator_loss_for_given_epoch += discriminator_loss.item()

            self.discriminator_optimizer.zero_grad()

            discriminator_loss.backward()

            self.discriminator_optimizer.step()

            discriminator_metric = self.discriminator_metric_fn(discriminator_predicted_labels, discriminator_labels)

            # Update generator weights
            self.discriminator.eval()
            self.generator.train()
            
            y_pred = self.generator(x)

            generator_loss = self.generator_loss_fns[0](y_pred, y) + self.generator_loss_fns[1](self.discriminator(y_pred),torch.ones((y.shape[0], 1)))
            generator_loss_for_given_epoch += generator_loss.item()
            
            self.generator_optimizer.zero_grad()
            
            generator_loss.backward()
            
            self.generator_optimizer.step()
            
            generator_metric = self.generator_metric_fn(y_pred, y)

            # Display loss and metric values for the current batch
            loop.set_postfix(d_loss = discriminator_loss.item(),
                     d_metric = discriminator_metric.item(),
                     g_loss = generator_loss.item(), 
                     g_metric = generator_metric.item())

        # Compute the loss and metric values for the given epoch
        discriminator_loss_for_given_epoch /= len(self.train_dataloader)
        generator_loss_for_given_epoch /= len(self.train_dataloader)

        discriminator_metric_for_given_epoch = self.discriminator_metric_fn.compute()
        self.discriminator_metric_fn.reset()
        generator_metric_for_given_epoch = self.generator_metric_fn.compute()
        self.generator_metric_fn.reset()

        return discriminator_loss_for_given_epoch, generator_loss_for_given_epoch, discriminator_metric_for_given_epoch, generator_metric_for_given_epoch

    def train(self):
        
        results = { "discriminator_train_loss": [],
                  "generator_train_loss": [],
                   "discriminator_train_metric" : [],
                   "generator_train_metric": []
                }

        for epoch in range(self.epochs):
            
            print(f"Epoch {epoch + 1}/{self.epochs}: ")

            discriminator_loss, generator_loss, discriminator_metric, generator_metric = self.train_step()

            print(f"Epoch {epoch + 1} | Discriminator train loss {discriminator_loss} | Discriminator train metric {discriminator_metric} | Generator train loss {generator_loss} | Generator train metric {generator_metric}")

            results["discriminator_train_loss"].append(discriminator_loss)
            results["generator_train_loss"].append(generator_loss)
            results["discriminator_train_metric"].append(discriminator_metric)
            results["generator_train_metric"].append(generator_metric)

        return results

