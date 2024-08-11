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
    def __getitem__(cls, item) -> NoticeBoard:
        if item not in cls._boards:
            if item in cls._board_names:
                cls._boards[item] = cls()
            else:
                raise KeyError(f"Board {item} not found in board name list {cls._board_names}")
        return cls._boards[item]

    def __init__(self, board_name, board_url):
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
