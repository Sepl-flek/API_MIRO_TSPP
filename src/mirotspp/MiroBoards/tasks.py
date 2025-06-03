import requests
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from MiroBoard import MiroBoard
from MiroBoards.models import Boards, Items


@shared_task
def add_sticker_to_miro(board_id, json_content, x=0, y=0):
    board = Boards.objects.get(id=board_id)
    api_token = board.api_key
    content = json_content.get("content")
    color = json_content.get("color", "light_yellow")
    shape = json_content.get("shape", "square")
    width = json_content.get("shape", 199)
    miro = MiroBoard(board_id=board.board_id, API_TOKEN=api_token)
    return miro.add_sticker(content, color, x, y, width, shape)

@shared_task
def add_text_to_miro(board_id, json_content, x=0, y=0):
    board = Boards.objects.get(id=board_id)
    api_token = board.api_key
    content = json_content.get("content")
    fontSize = json_content.get("fontSize", 14)
    miro = MiroBoard(board_id=board.board_id, API_TOKEN=api_token)
    return miro.add_text(content=content, fontSize=fontSize, x=x, y=y)

@shared_task
def add_image_to_miro(board_id, json_content, x=0, y=0):
    board = Boards.objects.get(id=board_id)
    api_token = board.api_key
    url = json_content.get("url")
    width = json_content.get("width", 540)
    miro = MiroBoard(board_id=board.board_id, API_TOKEN=api_token)
    return miro.add_image(url=url, x=x, y=y, width=width)


def to_update_items(board_id):
    board = Boards.objects.get(id=board_id)
    api_token = board.api_key
    miro = MiroBoard(board_id=board.board_id, API_TOKEN=api_token)
    items = miro.get_board_items()

    for item in items:
        item_id = item["id"]
        item_type = item["type"]
        x, y = item["position"]["x"], item["position"]["y"]
        content_json = {}

        if item_type == "sticky_note":
            content = item["data"]["content"]
            shape = item["data"]["shape"]
            color = item["style"]["fillColor"]
            width = int(item["geometry"]["width"])
            content_json = {"content": content, "shape": shape, "color": color, "width": width}
            type_field = "stick"

        elif item_type == "text":
            content = item["data"]["content"]
            fontSize = item["style"]["fontSize"]
            content_json = {"content": content, "fontSize": fontSize}
            type_field = "txt"

        elif item_type == "image":
            url = item["data"]["imageUrl"]
            width = item["geometry"]["width"]
            content_json = {"url": url, "width": width}
            type_field = "img"
        else:
            continue

        save_item.delay(item_id, x, y, content_json, board_id, type_field)


@shared_task
def save_item(item_id, x, y, content_json, board_id, type_field):
    try:
        obj = Items.objects.get(item_id=item_id)
        obj.x_coordinate = x
        obj.y_coordinate = y
        obj.content = content_json
        obj.save()
    except ObjectDoesNotExist as exc:
        if content_json:
            board = Boards.objects.get(id=board_id)
            obj = Items.objects.create(item_id=item_id, board=board, type=type_field, x_coordinate=x, y_coordinate=y,
                                       content=content_json)