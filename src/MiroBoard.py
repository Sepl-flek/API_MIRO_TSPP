import json
import os

import requests


class MiroBoard:

    def __init__(self, board_id: str, API_TOKEN: str):
        self.board_id = board_id
        self.API_TOKEN = API_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "accept": "application/json",
            "content-type": "application/json",
        }
        self.url = f"https://api.miro.com/v2/boards/{self.board_id}/"

    def add_sticker(self, content, color="light_yellow", x=0, y=0):
        data = {
            "data": {"content": content},
            "position": {"x": x, "y": y},
            "style": {"fillColor": color},
        }

        url = self.url + "sticky_notes"
        try:
            response = requests.post(url, headers=self.headers, json=data)
            return json.loads(response.content)["id"]

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def add_image(self, url, x=0, y=0):
        data = {
            "data": {"url": url},
            "position": {"x": x, "y": y},
        }

        url = self.url + "images"
        try:
            response = requests.post(url, headers=self.headers, json=data)
            return json.loads(response.content)["id"]

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def add_text(self, content, fontSize=14, x=0, y=0):
        data = {
            "data": {"content": content},
            "position": {"x": x, "y": y},
            "style": {"fontSize": fontSize},
        }

        url = self.url + "texts"
        try:
            response = requests.post(url, headers=self.headers, json=data)
            return json.loads(response.content)["id"]

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def get_sticker(self, item_id, path=''):

        url = self.url + "sticky_notes/" + item_id

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = json.loads(response.content)['data']

            filename = f"sticker_{item_id}.txt"
            if path:
                filepath = os.path.join(path, filename)
            else:
                filepath = filename

            with open(filepath, 'w', encoding='UTF-8') as file:
                file.write(f'content: {data['content']}\n')
                file.write(f'shape: {data['shape']}')

            return True
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False

    def get_image(self, item_id, path=''):

        url = self.url + "images/" + item_id
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            image_url = json.loads(response.content)['data']['imageUrl']

            intermediate_response  = requests.get(image_url, headers=self.headers)
            intermediate_response .raise_for_status()

            intermediate_data = intermediate_response.json()
            final_image_url = intermediate_data['url']

            image_response = requests.get(final_image_url)
            image_response.raise_for_status()

            filename = f"image_{item_id}.png"
            if path:
                filepath = os.path.join(path, filename)
            else:
                filepath = filename

            with open(filepath, 'wb') as file:
                file.write(image_response.content)

            return True

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False

    def get_text(self, item_id, path=''):

        url = self.url + "texts/" + item_id
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            text = json.loads(response.content)['data']['content']

            filename = f"text_{item_id}.txt"
            if path:
                filepath = os.path.join(path, filename)
            else:
                filepath = filename

            with open(filepath, 'w', encoding='UTF-8') as file:
                file.write(text)

            return True
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False
