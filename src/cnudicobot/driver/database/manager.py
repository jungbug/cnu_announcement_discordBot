from typing import Tuple

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..env.settings import TargetBoardURLS

from .base import SessionLocal
from . import scheme as model

db: Session = SessionLocal()


def rollback():
    db.rollback()


def create_board(board_name: str) -> model.Boards | None:
    new_board = model.Boards(name=board_name, last_post_id=0)
    try:
        db.add(new_board)
        db.commit()
        db.refresh(new_board)
    except IntegrityError:
        new_board = None
        rollback()
    return new_board


def get_last_post_id(board_name: str) -> Tuple[int | None, model.Boards | None]:
    board: model.Boards = db.query(model.Boards).filter(model.Boards.name == board_name).first()
    if board is None:
        return -1, None
    elif board.last_post_id is 0:
        return None, board
    else:
        return board.last_post_id, board


def update_last_post_id(new_post_id: int, board_name: str | None = None, board_obj: model.Boards | None = None):
    if board_obj is None:
        if board_name is None:
            raise ValueError("Either board_name or board_obj should be provided.")
        _, board_obj = get_last_post_id(board_name)
    board_obj.last_post_id = new_post_id
    db.commit()
    db.refresh(board_obj)


for _board_name in TargetBoardURLS:
    create_board(_board_name)
