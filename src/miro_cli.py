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

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
