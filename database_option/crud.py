# 数据库操作
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, database


# Dependency
def get_db() -> Session:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_conversation_by_id(db: Session, id: str) -> models.Conversation:
    return db.query(models.Conversation).filter(models.Conversation.id == id).first()


def get_conversations(db: Session) -> List[models.Conversation]:
    return db.query(models.Conversation).all()


def insert_conversation(db: Session, conversation: schemas.ConversationInsert):
    db_item = models.Conversation(**conversation.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_conversation(db: Session, id:str, messages:list , new_id:str, consume_token:List[int]):
    object = get_conversation_by_id(db, id)
    object.id = new_id
    object.contents = messages
    object.consume_token.extend(consume_token)
    db.commit()
    db.refresh(object)
    return object
