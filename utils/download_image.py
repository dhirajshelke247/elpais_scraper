import requests
import os

def download_image(url, directory, filename):
    response = requests.get(url)
    path = os.path.join(directory, filename)
    with open(path, "wb") as f:
        f.write(response.content)
    return path
