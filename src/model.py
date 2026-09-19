import torch
import torch.nn.functional as F

def load_model():
    """
    Loads a ResNet-20 model pre-trained natively on CIFAR-10.
    """
    # Load model from torch hub
    model = torch.hub.load("chenyaofo/pytorch-cifar-models", "cifar10_resnet20", pretrained=True, trust_repo=True)
    model.eval()
    return model

def predict(model, device, image_tensor):
    """
    Runs inference on a batch of images.
    Returns predicted classes and their confidence (softmax probability).
    """
    with torch.no_grad():
        image_tensor = image_tensor.to(device)
        logits = model(image_tensor)
        probs = F.softmax(logits, dim=1)
        confidences, predicted_classes = torch.max(probs, dim=1)
    return predicted_classes.cpu().numpy(), confidences.cpu().numpy()
