from fastapi import Depends, FastAPI, HTTPException, Form, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt

from loguru import logger

from sql_app import secret_key

# to get a string like this run: 使用下面的命令获取一个随机的密钥
# openssl rand -hex 32
ALGORITHM = "HS256"
SECRET_KEY = secret_key.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = 30


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Welcome"}


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, user_name=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.get("/user/me/", response_model=schemas.UserBase)
async def read_user_me(current_user: schemas.UserBase = Depends(get_current_user)):
    return current_user


@app.post("/user/create_user")
async def create_user(username: str = Form(), password: str = Form(), db: Session = Depends(get_db),
                      current_user: schemas.UserBase = Depends(get_current_user)):
    logger.debug('用户名为' + str(current_user.user_name))
    logger.debug('用户权限为' + str(current_user.authority))
    if current_user.authority >= 4:
        res = crud.create_user(db, user_name=username, password=password, authority=7)
        return res
    else:
        return "权限不足"


# 以下为业务代码


@app.post("/material/add")
async def add_material(new_material: schemas.MaterialBase, db: Session = Depends(get_db),
                       current_user: schemas.UserBase = Depends(get_current_user)):
    logger.debug('用户名为' + str(current_user.user_name))
    logger.debug('用户权限为' + str(current_user.authority))
    if current_user.authority >= 2:
        res = crud.add_material(db, material_name=new_material.material_name, material_lot=new_material.material_lot,
                                material_EOV=new_material.material_EOV)
        return res
    else:
        return "权限不足"


@app.post("/equipments/add")
async def add_equipments(new_equipments: schemas.EquipmentsBase, db: Session = Depends(get_db),
                         current_user: schemas.UserBase = Depends(get_current_user)):
    logger.debug('用户名为' + str(current_user.user_name))
    logger.debug('用户权限为' + str(current_user.authority))
    if current_user.authority >= 2:
        res = crud.add_equipments(db, equipName=new_equipments.equipName, equipNum=new_equipments.equipNum,
                                  place=new_equipments.place)
        return res
    else:
        return "权限不足"


@app.post("/material/del")
async def del_material(del_id: int, db: Session = Depends(get_db),
                       current_user: schemas.UserBase = Depends(get_current_user)):
    logger.debug('用户名为' + str(current_user.user_name))
    logger.debug('用户权限为' + str(current_user.authority))
    if current_user.authority >= 2:
        res = crud.del_material(db, del_id)
        return "删除" + str(res) + "条成功"
    else:
        return "权限不足"


@app.post("/equipments/del")
async def del_equipments(del_id: int, db: Session = Depends(get_db),
                         current_user: schemas.UserBase = Depends(get_current_user)):
    logger.debug('用户名为' + str(current_user.user_name))
    logger.debug('用户权限为' + str(current_user.authority))
    if current_user.authority >= 2:
        res = crud.del_equipments(db, del_id)
        return "删除" + str(res) + "条成功"
    else:
        return "权限不足"


@app.get("/material/get_all")
async def read_material(db: Session = Depends(get_db)):
    res = crud.get_material_all(db)
    return res


@app.get("/equipments/get_all")
async def read_equipments(db: Session = Depends(get_db)):
    res = crud.get_equipments_all(db)
    return res


@app.post("/material/update")
async def update_material(new_material: schemas.MaterialBase, db: Session = Depends(get_db),
                          current_user: schemas.UserBase = Depends(get_current_user)):
    logger.debug('用户名为' + str(current_user.user_name))
    logger.debug('用户权限为' + str(current_user.authority))
    if current_user.authority >= 2:
        res = crud.update_material(db, material_id=new_material.material_id, material_name=new_material.material_name,
                                   material_lot=new_material.material_lot, material_EOV=new_material.material_EOV)
        return res
    else:
        return "权限不足"


@app.post("/equipments/update")
async def update_material(new_equipments: schemas.EquipmentsBase, db: Session = Depends(get_db),
                          current_user: schemas.UserBase = Depends(get_current_user)):
    logger.debug('用户名为' + str(current_user.user_name))
    logger.debug('用户权限为' + str(current_user.authority))
    if current_user.authority >= 2:
        res = crud.update_equipments(db, equipments_id=new_equipments.equipments_id, equipName=new_equipments.equipName,
                                     equipNum=new_equipments.equipNum, place=new_equipments.place)
        return res
    else:
        return "权限不足"
