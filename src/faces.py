import torch
from typing import Tuple
from facenet_pytorch import MTCNN
from torchvision.transforms.functional import to_pil_image, to_tensor

# Prevent gradients from being calcluated globally
torch.autograd.set_grad_enabled(False)

# Set Device
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
print(device)

# Load model
net = MTCNN(device=device)


def detect_faces(im) -> Tuple[torch.Tensor, torch.Tensor]:
    """Returns bounding boxes and confidence for a given pil Image"""
    # Enforce 3 channels
    im = to_tensor(im)[:3]
    im = to_pil_image(im)
    res = net.detect(im)
    # Check if no results
    if len(res) < 1:
        return [], []
    return res[0], res[1]
