from functools import cache

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database
SQLALCHEMY_DATABASE_URL = "sqlite:///sqlite.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Database models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text)
    count = Column(Integer)


Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


# API endpoints
@app.get("/")
async def root():
    return {"data": "Hello World"}


@app.post("/name")
async def show_name(name: str):
    return {"data": f"Hello {name}"}


@app.post("/name-cached")
@cache
async def show_name_cached(name: str):
    return {"data": f"Hello {name}"}


@app.post("/name-count")
async def show_name_count(name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == name).first()
    if not user:
        user = User(name=name, count=0)
    else:
        user.count += 1

    db.add(user)
    db.commit()
    return {"data": f"Hello {name} you was show {user.count} times"}
