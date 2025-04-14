import requests


class MiroBoard:

    def __init__(self, board_id: str, API_TOKEN: str):
        self.board_id = board_id
        self.API_TOKEN = API_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "accept": "application/json",
            "content-type": "application/json"
        }
        self.url = f"https://api.miro.com/v2/boards/{self.board_id}/"

    def add_sticker(self, content, color='light_yellow', x=0, y=0):
        data = {'data': {'content': content},
                'position': {'x': x, 'y': y},
                'style': {'fillColor': color}, }

        need_url = self.url + 'sticky_notes'
        response = requests.post(need_url, headers=self.headers, json=data)

        return response.status_code

    def add_image(self, url, x=0, y=0):
        data = {'data': {'url': url},
                'position': {'x': x, 'y': y}, }

        need_url = self.url + 'images'
        response = requests.post(need_url, headers=self.headers, json=data)

        return response.status_code

    def add_text(self, content, fontSize=14, x=0, y=0):
        data = {'data': {'content': content},
                'position': {'x': x, 'y': y},
                'style': {'fontSize': fontSize}, }

        need_url = self.url + 'texts'
        response = requests.post(need_url, headers=self.headers, json=data)

        return response.status_code
