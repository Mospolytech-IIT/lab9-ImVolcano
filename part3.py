"Файл для выполнения третьей части лабораторной работы (Страницы лежат в папке html)"

from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from sqlalchemy import create_engine
from sqlalchemy import  Column, Integer, String, ForeignKey

from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse

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

SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
def root():
    return FileResponse("html/index.html")

@app.get("/users")
def users():
    return FileResponse("html/users.html")

@app.get("/posts")
def posts():
    return FileResponse("html/posts.html")

@app.get("/api/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/api/users/{id}")
def get_user(id, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    return user

@app.post("/api/users")
def create_user(data  = Body(), db: Session = Depends(get_db)):
    user = User(username=data["username"], email=data["email"], password=data["password"])
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.put("/api/users")
def edit_user(data  = Body(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data["id"]).first()
    user.email = data["email"]
    user.username = data["username"]
    user.password = data["password"]
    db.commit() 
    db.refresh(user)
    return user

@app.delete("/api/users/{id}")
def delete_user(id, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    db.delete(user)
    db.commit()
    return user

@app.get("/api/posts")
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()

@app.get("/api/posts/{id}")
def get_post(id, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    return post

@app.post("/api/posts")
def create_post(data  = Body(), db: Session = Depends(get_db)):
    post = Post(title=data["title"], content=data["content"], user_id=data["user_id"])
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.put("/api/posts")
def edit_post(data  = Body(), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == data["id"]).first()
    post.content = data["content"]
    post.title = data["title"]
    post.user_id = data["user_id"]
    db.commit()
    db.refresh(post)
    return post

@app.delete("/api/posts/{id}")
def delete_post(id, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    db.delete(post)
    db.commit()
    return post
