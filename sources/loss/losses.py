import torch

class negativeLogLoss(torch.nn.Module):

    def __init__(self):

        super().__init__()
        

    def forward(self, input, target):
        
        #print(input)
        clamped_input = torch.clamp(input, min = 1e-4)
        loss =  - (target * torch.log(clamped_input))

        #print(loss.mean().item())

        return loss.mean()
