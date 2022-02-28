from modules.core.source import Base
from sqlalchemy import Column, BIGINT, TEXT, INTEGER, REAL


class Book(Base):
    __tablename__ = 'books'
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    title = Column(TEXT, unique=True)
    author = Column(TEXT)
    num_available = Column(INTEGER)
    price = Column(REAL)

    def __repr__(self):
        return "<Book(id='%s',title='%s',author='%s',num_available='%s',price='%s')>" % (
            self.id, self.title, self.author, self.num_available, self.price)
