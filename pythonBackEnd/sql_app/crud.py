from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from passlib.context import CryptContext

from . import models, schemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def add_material(db: Session, material_name, material_lot, material_EOV):
    db_material = models.Material(material_name=material_name, material_lot=material_lot, material_EOV=material_EOV)
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


def add_equipments(db: Session, equipName, equipNum, place):
    db_equipments = models.Equipments(equipName=equipName, equipNum=equipNum, place=place)
    db.add(db_equipments)
    db.commit()
    db.refresh(db_equipments)
    return db_equipments


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(db: Session, user_name, password, authority):
    try:
        db_user = models.User(user_name=user_name, password_hash=get_password_hash(password), authority=authority)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        return "用户名不可重复"
    except SQLAlchemyError:
        return "数据错误"
    return '创建完成'


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, user_name, password):
    user = get_user(db, user_name=user_name)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


def get_material_all(db: Session):
    return db.query(models.Material).all()


def get_equipments_all(db: Session):
    return db.query(models.Equipments).all()


def get_user(db: Session, user_name: str):
    user = db.query(models.User).filter(models.User.user_name == user_name).one_or_none()
    return user


def update_material(db: Session, material_id: int, **kwargs):
    res = db.query(models.Material).filter(models.Material.id == material_id).update(kwargs)
    db.commit()
    return res


def update_equipments(db: Session, equipments_id: int, **kwargs):
    res = db.query(models.Equipments).filter(models.Equipments.id == equipments_id).update(kwargs)
    db.commit()
    return res


def del_material(db: Session, material_id: int):
    res = db.query(models.Material).filter(models.Material.id == material_id).delete()
    db.commit()
    return res


def del_equipments(db: Session, equipments_id: int):
    res = db.query(models.Equipments).filter(models.Equipments.id == equipments_id).delete()
    db.commit()
    return res

