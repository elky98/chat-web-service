# 表创建
import enum
from sqlalchemy import Boolean, Column, ForeignKey, Integer, TEXT, DATETIME, Float, Enum, JSON

from .database import Base


class PermissionsEnum(enum.Enum):
    administrator = "ADMINISTRATOR"
    user = "USER"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) # 用户id
    permissions = Column(Enum(PermissionsEnum)) # 用户权限
    email = Column(TEXT, unique=True, index=True) # 邮箱
    hashed_password = Column(TEXT) # 密码
    name = Column(TEXT) # 用户名
    create_time = Column(DATETIME) # 创建时间
    is_active = Column(Boolean, default=False) # 是否激活
    expiration_time = Column(DATETIME) # 到期时间
    conversation_count = Column(Integer) # 对话次数
    balance = Column(Float) # 余额
    memory_item = Column(Integer) # 记忆对话条数


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(TEXT, primary_key=True) # 会话id
    # user_id = Column(ForeignKey("users.id"), nullable=False) # 会话主id
    user_id = Column(Integer, nullable=True) # 会话主id
    title = Column(TEXT, index=True) # 标题
    contents = Column(JSON) # 会话内容
    create_time = Column(DATETIME) # 会话创建时间
    consume_token = Column(JSON) # 消耗的token数


class DiscountWayEnum(enum.Enum):
    anything = "ANGTHING"
    only_time = "ONLY_TIME"
    only_conversation = "ONLY_CONVERSSATION"
    only_balance = "ONLY_BALANCE"


class DiscountCode(Base):
    __tablename__ = "discount_codes"

    id = Column(TEXT, primary_key=True) # 折扣码
    discount_way = Column(Enum(DiscountWayEnum)) # 折扣方式
    anything_discount = Column(Float) # 任何方式的折扣
    time_discount = Column(Float) # 时长折扣
    conversation_count_discount = Column(Float) # 对话次数折扣
    balance_discount = Column(Float) # 余额折扣


class VoucherCodeType(enum.Enum):
    combo = "COMBO"
    time = "TIME"
    conversation = "CONVERSSATION"
    balance = "BALANCE"


class VoucherCode(Base):
    __tablename__ = "mouche_codes"

    id = Column(TEXT, primary_key=True) # 卡密id
    price = Column(Float) # 成交价
    discount_code = Column(ForeignKey("discount_codes.id")) # 折扣码
    type = Column(Enum(VoucherCodeType)) # 卡密类型，组合卡, 时长卡，对话次数卡，余额卡
    time = Column(Float) # 时长
    conversation_count = Column(Integer) # 对话次数
    balance = Column(Float) # 余额
    purchase_time = Column(DATETIME) # 购买时间
    expiration_time = Column(DATETIME) # 过期时间
    creator_id = Column(ForeignKey("users.id")) # 创建者id
    owner_id = Column(ForeignKey("users.id")) # 拥有者id
    used_id = Column(ForeignKey("users.id")) # 充值者id
    used_time = Column(DATETIME) # 核销时间


class SaleCombo(Base):
    __tablename__ = "sale_combos"

    id = Column(TEXT, primary_key=True) # 组合id
    price = Column(Float) # 定价
    time = Column(Float)  # 包含的时长
    conversation_count = Column(Integer)  # 包含的对话次数
    balance = Column(Float)  # 包含的余额
    total_share = Column(Integer) # 份额
    create_time = Column(DATETIME) # 创建时间
    end_time = Column(DATETIME) # 结束时间
    discount = Column(Float) # 折扣
    describe = Column(TEXT) # 描述