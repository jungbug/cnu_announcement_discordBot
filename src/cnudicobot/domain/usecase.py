##############################
# Use case for the discord bot
##############################
from ..adapter.presenter.transmitter import setup_transmitter, get_channel_id, notify
from ..adapter.controller.noticeboard import NoticeBoard


def register_task(operator: callable) -> callable:
    """ Register the task to the transmitter """
    runner = setup_transmitter(task=operator)
    return runner


def register_notice_board() -> list[callable]:
    """ Register the notice board """
    notice_boards = NoticeBoard.get_instance(board_name=None)

    def task_setup(board: NoticeBoard):
        async def wrapped(get_channel):
            await operate_single_transmission(board, get_channel)
        return wrapped

    return [task_setup(board) for board in notice_boards]


async def operate_single_transmission(board: NoticeBoard, get_channel: callable):
    """ Operate the single notice board transmission """
    board_channel_id = get_channel_id(board.name)
    new_posts = board.get_new_posts()

    if new_posts:
        channel = get_channel(board_channel_id)

        for post_id, post in new_posts.items():
            await notify(channel, title=post['title'], content_tags=post['tags'], contents=post['contents'])
