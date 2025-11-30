# model.py
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

class DenseNetCustom(nn.Module):
    def __init__(self, num_classes=2):
        super().__init__()
        weights = models.DenseNet121_Weights.IMAGENET1K_V1
        self.densenet = models.densenet121(weights=weights)

        # Replace classifier for 2-class task (real vs fake)
        self.densenet.classifier = nn.Linear(1024, num_classes)

    def forward(self, x):
        return self.densenet(x)

# Image transform for training/inference
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406], 
        std=[0.229, 0.224, 0.225]
    )
])

# Device
device = "cuda" if torch.cuda.is_available() else "cpu"
