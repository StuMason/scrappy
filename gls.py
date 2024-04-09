# Get a png from https://localhost:4566/test/ and save it to /images
import os
import requests
import time
import traceback
import sys

def download_image(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
            print(f"Downloaded {file_name}")
    else:
        print(f"Failed to download {file_name}")


def main(filename):
    url = f"http://localhost:4566/test/{filename}.png"
    download_image(url, f"tests/_fixtures/{filename}.png")

if __name__ == "__main__":
    filename = sys.argv[1]
    print(f"Downloading {filename}")
    main(filename)
