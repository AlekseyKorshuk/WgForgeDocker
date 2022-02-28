import functools
from modules.core.source import Session
from modules.database.classes import Book


# decorator to give function session for db read and close connection
def db_read(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        session = Session()
        ret = function(session, *args, **kwargs)
        session.close()
        return ret

    return wrapper


# decorator to give function session for db write, commit and close connection
def db_write(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        session = Session()
        ret = function(session, *args, **kwargs)
        session.commit()
        session.close()
        return ret

    return wrapper


@db_write
def add_book(session, title: str, author: str, num_available: int, price: int):
    ed_book = Book(
        title=title,
        author=author,
        num_available=num_available,
        price=price
    )
    session.add(ed_book)
    # session.commit()


@db_read
def get_all_books(session):
    return session.query(Book).all()


@db_write
def delete_book(session, title: str, author: str):
    try:
        obj = session.query(Book).filter(Book.title == title and Book.author == author).first()
        session.delete(obj)
        return True
    except:
        return False
