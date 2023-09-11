from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint

from .database import Base


class Material(Base):
    """
    创建物料信息数据表模板
    """
    __tablename__ = "Material"

    id = Column(Integer, primary_key=True, autoincrement=True)
    material_name = Column(String)  # 物料名称
    material_lot = Column(String)  # 物料批号
    material_EOV = Column(String)  # 有效期

    __table_args__ = (UniqueConstraint('material_name', 'material_lot'),)


class Equipments(Base):
    """
    创建设备信息数据表模板
    """
    __tablename__ = "Equipments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    equipName = Column(String)
    equipNum = Column(String)
    place = Column(String)

    __table_args__ = (UniqueConstraint('equipName', 'equipNum'),)


class User(Base):
    """
    创建用户信息模板
    """
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, unique=True)
    password_hash = Column(String)
    # 1为上传报告的权限，2为修改物料设备信息的权限，4为增加新用户的权限，可累加
    authority = Column(Integer)


