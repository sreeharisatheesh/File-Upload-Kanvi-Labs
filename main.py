from fastapi import FastAPI, Request, Form, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import List
import shutil, os

import models
from database import engine, get_session

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(request: Request, db: Session = Depends(get_session)):
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.get("/", response_class=HTMLResponse)
def read_root():
    return RedirectResponse(url="/login")

@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
def register(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_session)):
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {"request": request, "msg": "User already exists"})
    user = models.User(username=username, hashed_password=get_password_hash(password))
    db.add(user)
    db.commit()
    return RedirectResponse(url="/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/token", response_class=HTMLResponse)
def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "msg": "Incorrect username or password"})
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    response = RedirectResponse(url="/uploadfile", status_code=303)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@app.get("/uploadfile", response_class=HTMLResponse)
def upload_file_form(request: Request, user: models.User = Depends(get_current_user), db: Session = Depends(get_session)):
    files = db.query(models.File).filter(models.File.owner_id == user.id).all()
    return templates.TemplateResponse("uploadfile.html", {"request": request, "files": files})

@app.post("/uploadfile")
def upload_files(request: Request, files: List[UploadFile] = File(...), user: models.User = Depends(get_current_user), db: Session = Depends(get_session)):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    for uploaded_file in files:
        file_location = os.path.join(upload_dir, uploaded_file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
        new_file = models.File(filename=uploaded_file.filename, owner_id=user.id)
        db.add(new_file)
    db.commit()
    return RedirectResponse(url="/uploadfile", status_code=303)

@app.get("/download/{filename}")
def download_file(filename: str, user: models.User = Depends(get_current_user), db: Session = Depends(get_session)):
    file_record = db.query(models.File).filter(models.File.filename == filename, models.File.owner_id == user.id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found or unauthorized")
    file_path = os.path.join("uploads", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
    return FileResponse(path=file_path, filename=filename, media_type="application/octet-stream")

@app.get("/delete/{filename}")
def delete_file(filename: str, user: models.User = Depends(get_current_user), db: Session = Depends(get_session)):
    file_entry = db.query(models.File).filter(models.File.filename == filename, models.File.owner_id == user.id).first()
    if not file_entry:
        raise HTTPException(status_code=404, detail="File not found")
    file_path = os.path.join("uploads", filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.delete(file_entry)
    db.commit()
    return RedirectResponse(url="/uploadfile", status_code=303)
