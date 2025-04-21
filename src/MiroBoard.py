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

    def get_sticker(self, item_id, path=""):

        url = self.url + "sticky_notes/" + item_id

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = json.loads(response.content)["data"]

            filename = f"sticker_{item_id}.txt"
            if path:
                filepath = os.path.join(path, filename)
            else:
                filepath = filename

            with open(filepath, "w", encoding="UTF-8") as file:
                file.write(f"content: {data['content']}\n")
                file.write(f"shape: {data['shape']}")

            return True
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False

    def get_image(self, item_id, path=""):

        url = self.url + "images/" + item_id
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            image_url = json.loads(response.content)["data"]["imageUrl"]

            intermediate_response = requests.get(image_url, headers=self.headers)
            intermediate_response.raise_for_status()

            intermediate_data = intermediate_response.json()
            final_image_url = intermediate_data["url"]

            image_response = requests.get(final_image_url)
            image_response.raise_for_status()

            filename = f"image_{item_id}.png"
            if path:
                filepath = os.path.join(path, filename)
            else:
                filepath = filename

            with open(filepath, "wb") as file:
                file.write(image_response.content)

            return True

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False

    def get_text(self, item_id, path=""):

        url = self.url + "texts/" + item_id
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            text = json.loads(response.content)["data"]["content"]

            filename = f"text_{item_id}.txt"
            if path:
                filepath = os.path.join(path, filename)
            else:
                filepath = filename

            with open(filepath, "w", encoding="UTF-8") as file:
                file.write(text)

            return True
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False

    def create_template(self, template_name, items):
        template_dir = "templates"
        if not os.path.exists(template_dir):
            os.makedirs(template_dir)

        template_path = os.path.join(template_dir, f"{template_name}.json")
        try:
            with open(template_path, "w", encoding="UTF-8") as file:
                json.dump(items, file, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Template creation error: {e}")
            return False

    def get_board_items(self):
        try:
            response = requests.get(f"{self.url}items", headers=self.headers)
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            print(f"Failed to get board items: {e}")
            return []

    # TODO: image is not uploading to template
    # TODO: add size to image and stikers, now stikers uploading at base size
    def create_template_from_board(self, template_name, item_ids=None):
        try:
            all_items = []
            url = f"{self.url}items?limit=50"
            while url:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                all_items.extend(data.get("data", []))
                url = data.get("links", {}).get("next")

            if not all_items:
                print("No items found on the board")
                return False

            template_items = []
            for item in all_items:
                current_id = item.get("id")
                if item_ids and current_id not in item_ids:
                    continue

                template_item = {
                    "type": item.get("type"),
                    "position": item.get("position", {"x": 0, "y": 0}),
                    "style": item.get("style", {}),
                    "data": item.get("data", {}),
                }

                if item.get("type") == "image" and "geometry" in item:
                    template_item["geometry"] = item["geometry"]

                template_items.append(template_item)

            return self.create_template(template_name, template_items)

        except Exception as e:
            print(f"Error creating template: {e}")
            return False

    def export_template(self, template_name):
        template_path = os.path.join("templates", f"{template_name}.json")

        if not os.path.exists(template_path):
            return None

        try:
            with open(template_path, "r", encoding="UTF-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"Template export error: {e}")

    def import_template(self, template_name, position=None):
        template = self.export_template(template_name)
        if not template:
            print(f"Template '{template_name}' not found or could not be loaded")
            return False

        base_x = position.get("x", 0) if position else 0
        base_y = position.get("y", 0) if position else 0

        try:
            for item in template:
                if not isinstance(item, dict):
                    continue

                if "id" in item:
                    del item["id"]
                if "data" in item and "id" in item["data"]:
                    del item["data"]["id"]

                item_type = item.get("type")
                item_data = item.get("data", {})
                item_position = item.get("position", {})
                item_style = item.get("style", {})

                x = item_position.get("x", 0) + base_x
                y = item_position.get("y", 0) + base_y

                if item_type == "sticker" or item_type == "sticky_note":
                    self.add_sticker(
                        content=item_data.get("content", ""),
                        color=item_style.get("fillColor", "light_yellow"),
                        x=x,
                        y=y,
                    )
                elif item_type == "text":
                    self.add_text(
                        content=item_data.get("content", ""),
                        fontSize=item_style.get("fontSize", 14),
                        x=x,
                        y=y,
                    )
                elif item_type == "image":
                    image_url = item_data.get("url", "")
                    if not image_url:
                        continue

                    self.add_image(url=image_url, x=x, y=y)

            return True
        except Exception as e:
            print(f"Template import error: {e}")
            return False
