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

    def add_sticker(
        self, content, color="light_yellow", x=0, y=0, width=199, shape="square"
    ):
        data = {
            "data": {"content": content, "shape": shape},
            "position": {"x": x, "y": y},
            "style": {"fillColor": color},
            "geometry": {"width": width},
        }

        url = self.url + "sticky_notes"
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return json.loads(response.content)["id"]

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def add_image(self, url, x=0, y=0, width=540):
        data = {
            "data": {"url": url},
            "position": {"x": x, "y": y},
            "geometry": {"width": width},
        }

        url = self.url + "images"
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
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
            response.raise_for_status()
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
            geometry = json.loads(response.content)["geometry"]

            filename = f"sticker_{item_id}.txt"
            if path:
                filepath = os.path.join(path, filename)
            else:
                filepath = filename

            with open(filepath, "w", encoding="UTF-8") as file:
                file.write(f"content: {data['content']}\n")
                file.write(f"shape: {data['shape']}\n")
                file.write(f"width: {geometry['width']}\n")

            return True
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False

    def get_image(self, item_id, path=""):

        url = self.url + "images/" + item_id
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            data = json.loads(response.content)["data"]
            geometry = json.loads(response.content)["geometry"]

            image_url = json.loads(response.content)["data"]["imageUrl"]

            intermediate_response = requests.get(image_url, headers=self.headers)
            intermediate_response.raise_for_status()

            intermediate_data = intermediate_response.json()
            final_image_url = intermediate_data["url"]

            image_response = requests.get(final_image_url)
            image_response.raise_for_status()

            filename = f"image_{item_id}.png"
            filename_info = f"info_image_{item_id}.txt"
            if path:
                filepath = os.path.join(path, filename)
                filepath_info = os.path.join(path, filename_info)
            else:
                filepath = filename
                filepath_info = filename_info

            with open(filepath, "wb") as file:
                file.write(image_response.content)

            with open(filepath_info, "w", encoding="UTF-8") as file:
                file.write(f"imageUrl: {data['imageUrl']}\n")
                file.write(f"width: {geometry['width']}")
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

            template_dir = os.path.join("templates", template_name)
            images_dir = os.path.join(template_dir, "images")
            os.makedirs(images_dir, exist_ok=True)

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
                    "geometry": item.get("geometry", {}),
                }

                if item.get("type") == "image":
                    image_url = item["data"].get("imageUrl")
                    if image_url:
                        try:
                            response = requests.get(image_url, headers=self.headers)
                            response.raise_for_status()

                            if response.headers.get("Content-Type", "").startswith(
                                "image/"
                            ):
                                image_data = response.content
                            else:
                                json_data = response.json()
                                final_url = json_data.get("url")
                                if final_url:
                                    image_response = requests.get(final_url)
                                    image_response.raise_for_status()
                                    image_data = image_response.content
                                else:
                                    raise ValueError(
                                        "No valid image URL found in response"
                                    )

                            image_filename = f"image_{current_id}.png"
                            image_path = os.path.join(images_dir, image_filename)
                            with open(image_path, "wb") as file:
                                file.write(image_data)

                            template_item["local_image"] = image_filename
                            template_item["data"]["url"] = image_url

                        except Exception as e:
                            print(f"Failed to download image {current_id}: {e}")
                            continue

                elif item.get("type") in ["sticker", "sticky_note"]:
                    if "geometry" not in template_item:
                        template_item["geometry"] = {"width": 199}

                template_items.append(template_item)

            template_path = os.path.join(template_dir, f"{template_name}.json")
            try:
                with open(template_path, "w", encoding="UTF-8") as file:
                    json.dump(template_items, file, ensure_ascii=False, indent=4)
                return True
            except Exception as e:
                print(f"Template creation error: {e}")
                return False

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
        template_dir = os.path.join("templates", template_name)
        template_path = os.path.join(template_dir, f"{template_name}.json")

        if not os.path.isfile(template_path):
            print(f"Template '{template_name}' not found at {template_path}")
            return False

        try:
            with open(template_path, "r", encoding="utf-8") as file:
                template = json.load(file)
        except Exception as e:
            print(f"Failed to load template: {e}")
            return False

        base_x = position.get("x", 0) if position else 0
        base_y = position.get("y", 0) if position else 0

        for item in template:
            if not isinstance(item, dict):
                print(f"Skipping non-dict item: {item}")
                continue

            item_type = item.get("type")
            data = item.get("data", {})
            style = item.get("style", {})
            geometry = item.get("geometry", {})
            pos = item.get("position", {})

            x = pos.get("x", 0) + base_x
            y = pos.get("y", 0) + base_y

            try:
                if item_type in ["sticker", "sticky_note"]:
                    self.add_sticker(
                        content=data.get("content", ""),
                        color=style.get("fillColor", "light_yellow"),
                        x=x,
                        y=y,
                        width=geometry.get("width", 199),
                        shape=data.get("shape", "square"),
                    )

                elif item_type == "text":
                    self.add_text(
                        content=data.get("content", ""),
                        fontSize=style.get("fontSize", 14),
                        x=x,
                        y=y,
                    )

                elif item_type == "image":
                    image_width = geometry.get("width", 1200)
                    local_image = item.get("local_image")
                    remote_url = data.get("url")

                    if local_image:
                        image_path = os.path.join(template_dir, "images", local_image)
                        if not os.path.isfile(image_path):
                            print(f"Local image not found: {image_path}")
                        else:
                            try:
                                with open(image_path, "rb") as img_file:
                                    files = {
                                        "resource": (local_image, img_file, "image/png")
                                    }
                                    data_fields = {
                                        "position[x]": str(x),
                                        "position[y]": str(y),
                                        "geometry[width]": str(image_width),
                                    }

                                    headers = {
                                        "Authorization": f"Bearer {self.API_TOKEN}",
                                        "Accept": "application/json",
                                    }

                                    response = requests.post(
                                        f"{self.url}images",
                                        headers=headers,
                                        files=files,
                                        data=data_fields,
                                    )
                                    response.raise_for_status()
                                    print(f"Uploaded image '{local_image}'")
                                    continue
                            except Exception as e:
                                print(
                                    f"Failed to upload local image '{local_image}': {e}"
                                )

                    if remote_url:
                        self.add_image(url=remote_url, x=x, y=y, width=image_width)
                    else:
                        print(f"No valid image for item at ({x}, {y})")

            except Exception as e:
                print(f"Failed to process item: {e}")

        return True
