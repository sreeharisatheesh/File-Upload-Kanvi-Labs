# 📂 File-Upload-Kanvi-Labs

A secure and minimalistic file upload and download service built with **FastAPI**, using **SQLite** as the backend database via **SQLAlchemy**, and **Jinja2** for HTML templates. Developed for Kanvi Labs as a demonstration backend application.

![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)
![SQLite](https://img.shields.io/badge/SQLite-3.0+-003B57?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

---

## 📖 Table of Contents

- [📂 Features](#-features)
- [📁 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
- [📝 Tech Stack](#-tech-stack)
- [📌 Available Endpoints](#-available-endpoints)
- [📸 Screenshots](#-screenshots)
- [📄 License](#-license)
- [✨ Author](#-author)

---

## 📂 Features

✅ User registration and login  
✅ Secure file upload and download with file metadata storage  
✅ File validation (type, size can be extended)  
✅ SQLite database management with SQLAlchemy ORM  
✅ Jinja2 templating for frontend rendering  
✅ Clean, organized, modular code structure  

---

## 📁 Project Structure

File-Upload-Kanvi-Labs/ ├── fileupload/ # Uploaded files directory 
├── templates/ # HTML templates (login, register, upload) │ 
    ├── login.html │ 
    ├── register.html │ 
    └── uploadfile.html 
├── database.db # SQLite database file 
├── database.py # Database connection and session management 
├── main.py # FastAPI application routes 
├── models.py # SQLAlchemy ORM models 
└── pycache/ # Python cache files


## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/sreeharisatheesh/File-Upload-Kanvi-Labs.git
cd File-Upload-Kanvi-Labs
```


### 2️⃣ Install Required Dependencies

```bash
pip install fastapi uvicorn sqlalchemy jinja2
```



### 3️⃣ Run the Application

```bash
uvicorn main:app --reload --port 8000
```


### 4️⃣ Access the App

```bash
http://127.0.0.1:8000/
```


### 📝 Tech Stack

Backend: FastAPI
Database: SQLite with SQLAlchemy ORM
Templating: Jinja2
Language: Python 3.10+


