import torch
from facenet_pytorch import MTCNN
from torchvision.transforms.functional import to_pil_image, to_tensor

# Set Device
torch.autograd.set_grad_enabled(False)
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print(device)

# Load models
net = MTCNN(device=device)

def detect_faces(im):
    im = to_tensor(im)[:3] # Enforce 3 channels
    im = to_pil_image(im)
    return net.detect(im)[0]