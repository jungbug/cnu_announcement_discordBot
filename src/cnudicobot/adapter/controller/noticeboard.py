##############################
# Notice Board Data Controller
##############################
from __future__ import annotations

from ...driver.database import manager
from ...driver.env.settings import TargetBoardURLS


class NoticeBoard:
    """
    Notice Board Data Controller
    """

    _boards = dict()
    _board_names = tuple(TargetBoardURLS.keys())
    _board_urls = TargetBoardURLS

    @classmethod
    def get_instance(cls, board_name: str | None) -> NoticeBoard | list[NoticeBoard]:
        if board_name is None:
            return [cls.get_instance(name) for name in cls._board_names]
        elif board_name not in cls._boards:
            if board_name in cls._board_names:
                cls._boards[board_name] = cls(board_name, cls._board_urls[board_name])
            else:
                raise KeyError(f"Board {board_name} not found in board name list {cls._board_names}")
        return cls._boards[board_name]

    def __init__(self, board_name: str, board_url: str):
        self._name = board_name
        self._board_url = board_url
        self._get_last_post_id = lambda: manager.get_last_post_id(self._name)
        self._set_last_post_id = lambda new_post_id: manager.update_last_post_id(new_post_id, self._name)

    @property
    def name(self):
        return self._name

    @property
    def board_url(self):
        return self._board_url

    @property
    def last_post_id(self) -> int | None:
        _id, _ = self._get_last_post_id()
        if _id == 0:
            return None
        return _id

    def get_new_posts(self) -> dict[int: dict] | None:
        # get updated posts indexed from last_post_id to latest
        # if last_post_id is None, get just last post
        last_post_id, board_obj = self._get_last_post_id()
        new_posts = {}  # TODO: Implement get_new_posts by using web scraping
        new_last_post_id = tuple(new_posts.keys())[-1] if new_posts else None

        # apply updated status to db
        if new_last_post_id:
            self._set_last_post_id(new_last_post_id)

        # return new posts
        return new_posts
