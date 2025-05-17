from celery import shared_task

from MiroBoard import MiroBoard
from MiroBoards.models import Boards


# todo shared_task: run redis server
def add_sticker_to_miro(board_id, json_content, x=0, y=0):
    board = Boards.objects.get(id=board_id)
    api_token = board.api_key
    content = json_content.get("content")
    color = json_content.get("color", "light_yellow")
    shape = json_content.get("shape", "square")
    width = json_content.get("shape", 199)
    miro = MiroBoard(board_id=board.board_id, API_TOKEN=api_token)
    return miro.add_sticker(content, color, x, y, width, shape)


def add_text_to_miro(board_id, json_content, x=0, y=0):
    board = Boards.objects.get(id=board_id)
    api_token = board.api_key
    content = json_content.get("content")
    fontSize = json_content.get("fontSize", 14)
    miro = MiroBoard(board_id=board.board_id, API_TOKEN=api_token)
    return miro.add_text(content=content, fontSize=fontSize, x=x, y=y)


def add_image_to_miro(board_id, json_content, x=0, y=0):
    board = Boards.objects.get(id=board_id)
    api_token = board.api_key
    url = json_content.get("url")
    width = json_content.get("width", 540)
    miro = MiroBoard(board_id=board.board_id, API_TOKEN=api_token)
    return miro.add_image(url=url, x=x, y=y, width=width)
