# 数据库创建
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

database_dir = Path(__file__).parent.parent / "database"
database_dir.mkdir(parents=True, exist_ok=True)

database_file = database_dir / "chatgpt.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{database_file.as_posix()}"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

