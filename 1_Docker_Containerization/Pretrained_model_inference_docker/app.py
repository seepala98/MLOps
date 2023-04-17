import timm
import torch
import urllib
from PIL import Image
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform

import hydra 
from omegaconf import DictConfig

@hydra.main(config_path="config", config_name="config")
def app(cfg: DictConfig):
    model = timm.create_model(cfg.model, pretrained=True)
    model.eval()

    config = resolve_data_config({}, model=model)
    transform = create_transform(**config)

    url, filename = (cfg.filename, cfg.filename.split('/')[-1])
    urllib.request.urlretrieve(url, filename)
    img = Image.open(filename).convert('RGB')
    tensor = transform(img).unsqueeze(0) # transform and add batch dimension

    with torch.no_grad():
        out = model(tensor)
    probabilities = torch.nn.functional.softmax(out[0], dim=0)
    
    # Get imagenet class mappings
    url, filename = ("https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt", "imagenet_classes.txt")
    urllib.request.urlretrieve(url, filename)
    with open("imagenet_classes.txt", "r") as f:
        categories = [s.strip() for s in f.readlines()]

    # Print top categories per image
    top1_prob, top1_catid = torch.topk(probabilities, 1)

    final_output = {}
    for i in range(top1_prob.size(0)):
        final_output.update({"prediction": categories[top1_catid[i]], "confidence": format(top1_prob[i].item(), '.2f')})
    print(final_output)
    return final_output

if __name__ == '__main__':
    app()