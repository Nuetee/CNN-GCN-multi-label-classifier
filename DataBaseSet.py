import json
import requests
from io import BytesIO
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from PIL import Image

with open('./wikiart.json', 'r', encoding='UTF-8') as f:
    json_data = json.load(f)

data_list = json_data[2]["data"]

no_download_count = 0
replace_character = ['/', '\\', '*', ':', '?', '<', '>', '|', '"', '.']
for data in data_list:
    print(no_download_count)
    core_data = data["data"] if "data" in data else None
    
    if core_data == None or core_data == 'error':
        no_download_count += 1
        continue
    
    try:
        jsonObject = json.loads(core_data)
    except ValueError:
        print("Decoding JSON has failed.")
        no_download_count += 1
        continue
    
    image_id = data["image_id"]
    genre = ''
    media = ''
    style = ''

    imageURL = jsonObject["image"] if 'image' in jsonObject else None
    if imageURL == None or imageURL == 'error':
        no_download_count += 1
        continue
        
    genre = jsonObject["genre"] if 'genre' in jsonObject else ''
    style = jsonObject["style"] if 'style' in jsonObject else ''
    media = jsonObject["media"] if 'media' in jsonObject else ''
    

    for character in replace_character:
        genre = genre.replace(character, '')
        style = style.replace(character, '')
        media = media.replace(character, '')
        
    image_name = image_id + '+' + genre + '+' + style + '+'  + media + '.jpg'
    
    if len(image_name) > 200:
        continue

    file_path = './database_all/' + image_name
    response = requests.get(imageURL)
    img = Image.open(BytesIO(response.content))
    img = img.convert('RGB')
    img = img.resize((256, 256))
    img.save(file_path)
    
