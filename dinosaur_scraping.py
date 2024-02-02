import requests
from bs4 import BeautifulSoup
import time
import os, os.path

BASE_URL = f'https://www.nhm.ac.uk/discover/dino-directory/'
TARGET_RAW_LOCATION = f'./data_lake/raw/'

def safe_open_w(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w+')

def download_dino_file(dino_name):
    dino_url = BASE_URL + f'{dino_name}.html'
    html_page = requests.get(dino_url).text
    soup = BeautifulSoup(html_page, 'html.parser')
    mydivs = soup.find_all("div", {"class": "dinosaur--container"})

    first_letter = dino_name[0:1]
    file_location = TARGET_RAW_LOCATION + f'{first_letter}/{dino_name}.txt'
    with safe_open_w(file_location) as raw_file:
        raw_file.write(str(mydivs))

def download_dino_list(list_name):
    i = 0
    with open(list_name) as dino_file:
        for dino_name in dino_file:
            dino_name = dino_name.strip().lower()
            print(f" Downloading file #{i} for Dino: {dino_name}")
            download_dino_file(dino_name)
            time.sleep(10)
            i+=1
    
download_dino_list("dinosaur_list.txt")
