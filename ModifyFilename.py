import json
import os
import shutil

with open('./wikiart.json', 'r', encoding='UTF-8') as f:
    json_data = json.load(f)
data_list = json_data[2]["data"]
data_list = data_list[6578:]

replace_character = ['/', '\\', '*', ':', '?', '<', '>', '|', '"', '.']
legacy_path = './database_style'
new_path = './database_all/'

for data in data_list:
    core_data = data["data"] if "data" in data else None
    if core_data == None or core_data == 'error':
        continue

    try:
        jsonObject = json.loads(core_data)
    except ValueError:
        print("Decoding JSON has failed.")
        continue

    image_id = data["image_id"]
    genre = jsonObject["genre"] if 'genre' in jsonObject else ''
    style = jsonObject["style"] if 'style' in jsonObject else ''
    media = jsonObject["media"] if 'media' in jsonObject else ''

    for character in replace_character:
        genre = genre.replace(character, '')
        style = style.replace(character, '')
        media = media.replace(character, '')

    new_file_name = image_id + '+' + genre + '+' + style + '+' + media + '.jpg'

    if len(new_file_name) > 200:
        continue
    
    legacy_file = None
    for legacy_file_name in os.listdir(legacy_path):
        if legacy_file_name.startswith(image_id):
            src = os.path.join(legacy_path, legacy_file_name)
            stopover = os.path.join(legacy_path, new_file_name)
            dst = os.path.join(new_path, new_file_name)
            # 파일명 변경
            os.rename(src, stopover)
            shutil.move(stopover, dst)

    
