from tqdm import tqdm
import json
import copy
import requests
from pprint import pprint
import time

vk_token = input('Введите токен ВК АПИ: ')
id_user = input('Введите ID ВК: ')
url_vk = 'https://api.vk.com/method/photos.get'
ya_token = 'AQAAAAAIYbfQAADLW0FCHvbi6UvXh8ZDO8QGBHo'

class VK_user:
    def __init__(self):
         self.token = vk_token
         self.id = id_user
         self.url = url_vk
         
    def load_photo(self):
        params = {
        'access_token': self.token,
        'owner_id': self.id,
        'album_id': 'profile',
        'photo_sizes': 1,
        'extended': 1,
        'offset': 1,
        'count': 5,
        'v': 5.131
    }  
        res = requests.get(self.url, params=params).json()
        return res['response']['items']

    def get_dict_photo(self):
        photo_list = []
        Name_list = []
        photo_dict = {} 
        copy_photo_dict = {}
        self.url_photo = []
        for i in self.load_photo():
            name = i['likes']['count']
            url_photo = i['sizes'][-1]['url']
            if name not in Name_list:
                photo_dict["file_name"] = f"{name}.jpg"
                photo_dict['size'] = i['sizes'][-1]['type']
            
            Name_list.append(name)
            copy_photo_dict = copy.deepcopy(photo_dict)
            photo_list.append(copy_photo_dict)
            self.url_photo.append(url_photo)
            with open('photo_log.json', 'w') as write_file:
                json.dump(photo_list, write_file)
        return photo_list 

 
 

class YA_user:
    def __init__(self):
        self.ya_token = ya_token
            
    def ya_headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'OAuth {}'.format(self.ya_token)
        }

    def get_folder(self,folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        requests.put(url, headers=self.ya_headers(), params=params)
        print(f'\nПапка {folder_name} успешно создана в корневом каталоге Яндекс диска\n')

    def get_url_folder(self,folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        res = requests.get(url, headers=self.ya_headers, params=params).json()['_embedded']['items']
        url_list = []
        for i in res:
            url_list.append(i['name'])
        return url_list    

    def upload_photo(self,get_folder):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.ya_headers()
        with open('photo_log.json') as file_object:
            name_photo = json.load(file_object)
        for new_name_photo, url_photo in tqdm(zip(name_photo, VK.url_photo)):
            time.sleep(1)
            name = new_name_photo['file_name']
            params = {"path": f'ФОТКИ С ВК/{name}',
                      'url': url_photo}
            response = requests.post(upload_url, headers=headers, params=params)
            
            
if __name__ == '__main__':
    VK = VK_user()
    ya = YA_user()
    VK.get_dict_photo()
    ya.get_folder('ФОТКИ С ВК')
    ya.upload_photo(get_folder='ФОТКИ С ВК')