import argparse
import os
from MiroBoard import MiroBoard


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
    pass


def cmd_add_text(args):
    pass


def cmd_add_image(args):
    pass


def cmd_get_item(args):
    pass


def cmd_template_create(args):
    pass


def cmd_template_export(args):
    pass


def cmd_template_import(args):
    pass


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
