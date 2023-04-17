import json
import requests
from bs4 import BeautifulSoup
import urllib
from hurry.filesize import size

url = "https://download.pytorch.org/whl/torch_stable.html"
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, "html.parser")

urls = []
for link in soup.find_all('a'):
    # filter for linux cpu only and not manylinux and only torch and torchvision packages
    if link.get('href') is not None and link.get('href').endswith('.whl') and ("linux" in link.get('href') and not "manylinux" in link.get("href")) and ("cpu/" in link.get('href') and ("torch-" in link.get('href')) or ("torchvision-" in link.get('href'))):
        urls.append("https://download.pytorch.org/whl/"+link.get('href'))

url_dict = {}
for url in urls:
    req = urllib.request.Request(url, method="HEAD")
    f = urllib.request.urlopen(req)
    if url not in url_dict.keys():
        url_dict[url] = size(int(f.headers['Content-Length']))

# write to json file for later use
with open('url_dict.json', 'w') as fp:
    json.dump(url_dict, fp)

# read from json file
with open('url_dict.json', 'r') as fp:
    url_dict = json.load(fp)
    # keep only the once that has cp39 in the name and /cpu/
    url_dict = {k: v for k, v in url_dict.items() if "cpu" in k}
    url_dict = {k: v for k, v in url_dict.items() if "cp39" in k}
    # sort by size
    url_dict = {k: v for k, v in sorted(url_dict.items(), key=lambda item: item[1])}

print(url_dict)

# write to json file for later use 
with open('url_dict.json', 'w') as fp:
    json.dump(url_dict, fp)