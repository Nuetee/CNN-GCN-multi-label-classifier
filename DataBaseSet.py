import json
import requests
from io import BytesIO
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from PIL import Image

with open('./wikiart.json', 'r', encoding='UTF-8') as f:
    json_data = json.load(f)

data_list = json_data[2]["data"]
data_list = data_list[15642:]

# image_name = './database/NASA3 .jpg'
# f = open(image_name, 'wb')
# response = requests.get('https://uploads1.wikiart.org/images/magdalena-carmen-frieda-kahlo-y-calderón-de-rivera/a-few-small-nips-passionately-in-love-1935.jpg')
# img = Image.open(BytesIO(response.content))
# img.save(image_name)
# print(img.size[1])
# f.write(img)
# f.close()
# baseheight = 256

# data = data_list[1]
# core_data = data["data"]
# jsonObject = json.loads(core_data)
# print(type(jsonObject))
# print("image" in jsonObject)
# print("style" in jsonObject)


no_download_count = 0
replace_character = ['/', '\\', '*', ':', '?', '<', '>', '|', '"', '.']
for data in data_list:
    print(no_download_count)
    core_data = data["data"] if "data" in data else None
    if core_data == None or core_data == 'error':
        no_download_count += 1
        continue
    
    jsonObject = json.loads(core_data)
    
    image_id = data["image_id"]
    title = ''
    style = None

    imageURL = jsonObject["image"] if 'image' in jsonObject else None
    if imageURL == None or imageURL == 'error':
        no_download_count += 1
        continue
        
    title = jsonObject["title"] if 'title' in jsonObject else ''
    style = jsonObject["style"] if 'style' in jsonObject else None
    if style == None:
        no_download_count += 1
        continue
    

    for character in replace_character:
        title = title.replace(character, '')
        style = style.replace(character, '')
    # if image_id == '11928':
    #     title = 'Map of the Northern Sky with representations of the constellations'
    image_name = image_id + '+' + title + '+' + style + '.jpg'
    if len(image_name) > 198:
        over = len(image_name) - 198
        title = title[0:(len(title) - over)]
        image_name = image_id + '+' + title + '+' + style + '.jpg'
    file_path = './database_style/' + image_name
    # print(image_name)
    # print(imageURL)
    response = requests.get(imageURL)
    img = Image.open(BytesIO(response.content))
    img = img.convert('RGB')
    img = img.resize((256, 256))
    img.save(file_path)
    
