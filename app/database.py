from app.server import app
from functools import wraps
from .function import time
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sqlite3 , os , uuid

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.getcwd()}/files_storage_website.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Files(db.Model):
    __tablename__   = 'files'
    file_id         = db.Column(db.String(255),     primary_key=True,               nullable=False)
    user_id         = db.Column(db.String(255),                                     nullable=False)
    file_name       = db.Column(db.String(255),                                     nullable=False)
    file_password   = db.Column(db.String(255),                                     nullable=False)
    status          = db.Column(db.String(255),     default="Available")
    download_times  = db.Column(db.Integer    ,                                     nullable=False)
    create_date     = db.Column(db.DateTime,                                        nullable=False)
    expire_date     = db.Column(db.DateTime,                                        nullable=False)

    def __init__(self, file_id , user_id , file_name , file_password , create_date , expire_date ,download_times ) :
        self.file_id        = file_id
        self.user_id        = user_id
        self.file_name      = file_name
        self.file_password  = file_password 
        self.create_date    = create_date
        self.expire_date    = expire_date
        self.download_times = download_times

class FileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model           = Files
        load_instance   = True

class User(db.Model):
    __tablename__   = 'user'
    user_id         = db.Column(db.String(255),     primary_key=True,   nullable=False)
    username        = db.Column(db.String(255),     unique=True,        nullable=False)
    password        = db.Column(db.String(255),                         nullable=False)
    create_date     = db.Column(db.DateTime,        default="",         nullable=False)


    def __init__(self, user_id , username , password , create_date ) :
        self.user_id        = user_id
        self.username       = username
        self.password       = password
        self.create_date    = create_date 

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model           = User
        load_instance   = True
        
db.create_all()