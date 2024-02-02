from bs4 import BeautifulSoup
import os, os.path
import glob
import json

TARGET_RAW_LOCATION = f'./data_lake/raw/'
TARGET_JSON_LOCATION = f'./data_lake/json/'
class Dino(object): pass

def safe_open_w(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w+', encoding='utf-8')

def safe_get_array_text(array, index):
  try:
    return array[index].text
  except IndexError:
    return ''
  
def get_diet_era_country(content):
    for index, item in enumerate(content):
        if item == None:
           continue
        text = item.text
        if "Diet" in text:
          diet = content[index+2].text.lower().strip()
        if "lived" in text:
          era = content[index+2].text.lower().strip().split(',')[0]
        if "Found" in text:
          country = content[index+2].text.lower().strip()
    return diet, era, country

def parse_dino_file(dino_file):
    soup = BeautifulSoup(dino_file, 'html.parser')
    dino = Dino()
    dino.name = soup.find("h1", {"class": "dinosaur--name dinosaur--name-hyphenated"}).text.lower().strip()
    dino.name_pronunciation = soup.find("dd", { "class": "dinosaur--pronunciation" }).text.lower().strip()
    dino.name_meaning = soup.find("dd", { "class": "dinosaur--meaning" }).text.lower().strip().replace('\'', '')
    dino.image = soup.find("img", { "class": "dinosaur--image" }).attrs['src'].strip()
    dino.type = safe_get_array_text(soup.find("dl", { "class": "dinosaur--description dinosaur--list" }).contents, 3).lower().strip()
    dino.size = safe_get_array_text(soup.find("dl", { "class": "dinosaur--description dinosaur--list" }).contents, 7).lower().strip()
    dino.discovered = safe_get_array_text(soup.find("dl", { "class": "dinosaur--taxonomy dinosaur--list" }).contents, 7)[-5:-1].strip()
    
    info = soup.find("dl", { "class": "dinosaur--info dinosaur--list" }).contents
    dino.diet, dino.era, dino.country = get_diet_era_country(info)

    description = soup.find("div", { "class": "dinosaur--content-container layout-row" })
    dino.description = None if description == None else description.text.strip()

    return dino.__dict__

def save_dino_json(dino_json):
    file_location = TARGET_JSON_LOCATION + f'{dino_json["era"]}/{dino_json["name"]}.json'
    with safe_open_w(file_location) as json_file:
        json.dump(dino_json, json_file, ensure_ascii=False, indent=4)

def iterate_dino_files():
    subfolders = [ f.path for f in os.scandir(TARGET_RAW_LOCATION) if f.is_dir() ]
    for subfolder in subfolders:
        files = [f for f in glob.glob(f"{subfolder}/*.txt")]
        for file in files:
            with open(file) as dino_file:
                print(f"Starting file: {file}")
                dino_json = parse_dino_file(dino_file.read())
                save_dino_json(dino_json)

iterate_dino_files()