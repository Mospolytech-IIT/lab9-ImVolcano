"Файл для выполнения второй части лабораторной работы"

from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
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

# Функция для добавления нескольких записей в таблицу Users
def add_users():
    maxim = User(username="Maxim", email="mail@mail.ru", password="123456789")
    alexey = User(username="Alexey", email="alexey@mail.ru", password="qwerty")
    tom = User(username="Tom", email="tom@gmail.com", password="qazwsx123")
    db.add_all([maxim, alexey, tom])
    db.commit()

# Функция для добавления нескольких записей в таблицу Posts
def add_posts():
    post0 = Post(title="Videogames", content="I like play videogames!", user_id=1)
    post1 = Post(title="Cooking", content="I cooked something interesting)", user_id=3)
    post2 = Post(title="Study", content="I'm so tired", user_id=1)
    db.add_all([post0, post1, post2])
    db.commit()
# Функция для извлечения всех записей таблицы Users
def get_all_users():
    users = db.query(User).all()
    for user in users:
        print(f"{user.id} {user.username} {user.email} {user.password}")

# Функция для извлечения всех записей таблицы Posts с данными таблицы Users
def get_all_posts():
    posts = db.query(Post).all()
    for post in posts:
        print(f"Статью {post.title} написал пользователь {db.get(User, post.user_id).username}")

# Функция для извлечения всех записей таблицы Posts у определённого пользователя
def get_post(user_id):
    posts = db.query(Post).filter(Post.user_id == user_id).all()
    for post in posts:
        print(f"{post.title} {post.content}")

# Функция для обновления поля email у одной записи таблицы Users
def update_email(id, new_email):
    user = db.query(User).filter(User.id == id).first()
    user.email = new_email
    db.commit()
    print("Почта успешно изменена")

# Функция для обновления поля content у одной записи таблицы Posts
def update_content(id, new_content):
    post = db.query(Post).filter(Post.id == id).first()
    post.content = new_content
    db.commit()
    print("Содержание статьи успешно изменено")

# Функция для удаления одной записи таблицы Posts
def delete_post(id):
    post = db.query(Post).filter(Post.id == id).first()
    db.delete(post)
    db.commit()
    print("Пост удалён")

# Функция для удаления записи пользователя вместе со всеми его постами
def delete_user(id):
    user = db.query(User).filter(User.id == id).first()
    posts = db.query(Post).filter(Post.user_id == id).all()
    db.delete(user)
    for post in posts:
        db.delete(post)
    db.commit()
    print("Пользователь удалён вместе с его постами")

# Строка подключения
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Создание движка
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()

#add_users()

#add_posts()

#get_all_users()

#get_all_posts()

#get_post(1)

#update_email(1, "maks@mail.ru")

#update_content(3, "I'm very-very TIRED")

#delete_post(2)

#delete_user(1)
