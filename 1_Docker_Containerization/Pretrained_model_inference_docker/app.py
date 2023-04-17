import argparse
import json
import numpy as np
import timm
import torch
import urllib

from PIL import Image
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform

parser = argparse.ArgumentParser(description='PyTorch ImageNet Inference')
parser.add_argument("--model", metavar="model", default="resnet18", help = "model architecture")
parser.add_argument("--image", metavar="image", help = "image url")

def app():
    args = parser.parse_args()
    model = timm.create_model(args.model, pretrained=True)
    model.eval()

    url, filename = (args.image, args.image.split("/")[-1])
    urllib.request.urlretrieve(url, filename)

    config = resolve_data_config({}, model=model)
    transform = create_transform(**config)
    image = Image.open(filename).convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0)

    with torch.no_grad():
        output = model(image)
    probabilities = torch.nn.functional.softmax(output, dim=1)
    
    url, filename = ("https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt", "imagenet_classes.txt")
    urllib.request.urlretrieve(url, filename)
    with open(filename) as f:
        classes = [line.strip() for line in f.readlines()]

    top_probably, top_k = torch.topk(probabilities, k=1)
    for i in range(top_probably.size(0)):
        output = {"predicted": classes[top_k[i]], "probability": top_probably[i].item()}
        print(json.dumps(output))

if __name__ == "__main__":
    app()