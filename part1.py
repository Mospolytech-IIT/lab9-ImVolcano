"Файл для выполнения первой части лабораторной работы"

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import  Column, Integer, String, ForeignKey

class Base(DeclarativeBase): pass

# Таблица Users
class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

# Таблица Posts
class Post(Base):
    __tablename__ = "Posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey(User.id))

# Строка подключения
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Создание движка
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Создание таблиц
Base.metadata.create_all(bind=engine)
