from sqlalchemy import Column, Integer, String
from .base import Base as _Base
from .base import engine


class Boards(_Base):
    __tablename__ = "board"

    index = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    last_post_id = Column(Integer, index=True)


_Base.metadata.create_all(bind=engine)
