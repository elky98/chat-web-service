# 表数据类型格式化
import datetime
from pydantic import BaseModel
from typing import Union, List


class ConversationBase(BaseModel):
    id: str
    title: str
    contents: dict


class ConversationInsert(ConversationBase):
    user_id: Union[int | None]
    title:str
    contents: List[dict] # json
    create_time: datetime.datetime
    consume_token: List[int]


class ConversationUpdate(ConversationBase):
    title:str
    contents: str # json

