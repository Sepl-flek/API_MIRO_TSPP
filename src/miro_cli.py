import argparse
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from MiroBoard import MiroBoard

load_dotenv()


def _require(value, name):
    if value is None:
        raise SystemExit(f"reqired argiment {name} is not passed")


def _init_board(args) -> MiroBoard:
    api_token = args.token or os.getenv("MIRO_API_TOKEN")
    board_id = args.board or os.getenv("MIRO_BOARD_ID")
    _require(api_token, "MIRO_API_TOKEN")
    _require(board_id, "MIRO_BOARD_ID")

    return MiroBoard(str(board_id), str(api_token))


def cmd_add_sticker(args):
    board = _init_board(args)
    sticker_id = board.add_sticker(
        content=args.text,
        color=args.color,
        x=args.x,
        y=args.y,
        width=args.width,
        shape=args.shape,
    )
    print("sticker created:", sticker_id)


def cmd_add_text(args):
    board = _init_board(args)
    text_id = board.add_text(
        content=args.text,
        fontSize=args.size,
        x=args.x,
        y=args.y,
    )
    print("text created:", text_id)


def cmd_add_image(args):
    board = _init_board(args)
    img_id = board.add_image(
        url=args.url,
        x=args.x,
        y=args.y,
        width=args.width,
    )
    print("image added:", img_id)


def cmd_get_item(args):
    board = _init_board(args)
    ok = {
        "sticker": board.get_sticker,
        "image": board.get_image,
        "text": board.get_text,
    }[args.type](args.id, path=args.out)
    print("saved" if ok else "failed")


def cmd_template_create(args):
    board = _init_board(args)
    ok = board.create_template_from_board(args.name, item_ids=args.ids)
    print("template created" if ok else "failed")


def cmd_template_export(args):
    board = _init_board(args)
    template = board.export_template(args.name)
    if template:
        Path(f"{args.name}.json").write_text(
            json.dumps(template, ensure_ascii=False, indent=4), encoding="utf-8"
        )
        print(f"exported to {args.name}.json")
    else:
        print("template not found")


def cmd_template_import(args):
    board = _init_board(args)
    ok = board.import_template(args.name, position={"x": args.x, "y": args.y})
    print("template imported" if ok else "failed")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="miro_cli",
        description="CLI for miro",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("-t", "--token", help="API token miro ( MIRO_API_TOKEN )")
    p.add_argument("-b", "--board", help="board id ( MIRO_BOARD_ID )")

    sub = p.add_subparsers(dest="command", required=True)

    # sticker
    s = sub.add_parser("add_sticker", help="add sticker")
    s.add_argument("text")
    s.add_argument("--color", default="light_yellow")
    s.add_argument("--shape", default="square")
    s.add_argument("--width", type=int, default=199)
    s.add_argument("--x", type=int, default=0)
    s.add_argument("--y", type=int, default=0)
    s.set_defaults(func=cmd_add_sticker)

    # text
    s = sub.add_parser("add_text", help="add text block")
    s.add_argument("text")
    s.add_argument("--size", type=int, default=14)
    s.add_argument("--x", type=int, default=0)
    s.add_argument("--y", type=int, default=0)
    s.set_defaults(func=cmd_add_text)

    # image
    s = sub.add_parser("add_image", help="add image")
    s.add_argument("url")
    s.add_argument("--width", type=int, default=540)
    s.add_argument("--x", type=int, default=0)
    s.add_argument("--y", type=int, default=0)
    s.set_defaults(func=cmd_add_image)

    # template_create
    s = sub.add_parser("template_create", help="create template from board")
    s.add_argument("name")
    s.add_argument("--ids", nargs="*", help="list of item ids")
    s.set_defaults(func=cmd_template_create)

    # template_export
    s = sub.add_parser("template_export", help="export template to json")
    s.add_argument("name")
    s.set_defaults(func=cmd_template_export)

    # template_import
    s = sub.add_parser("template_import", help="import template")
    s.add_argument("name")
    s.add_argument("--x", type=int, default=0)
    s.add_argument("--y", type=int, default=0)
    s.set_defaults(func=cmd_template_import)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
