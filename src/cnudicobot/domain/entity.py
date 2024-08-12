##################################
# Entity class for the Discord Bot
##################################
import usecase


class NoticeDiscordBot:
    _object = None  # singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._object is None:
            cls._object = super(NoticeDiscordBot, cls).__new__(cls)
        return cls._object

    def __init__(self):
        """ Register use cases """
        self.runner = usecase.register_task(usecase.register_notice_board)

    def run(self):
        """ Run use cases """
        self.runner()
