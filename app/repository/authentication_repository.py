from flask              import jsonify
from ..server           import app
from flask_wtf          import FlaskForm
from wtforms            import StringField, TextField, SubmitField ,SelectField , PasswordField
from wtforms.validators import DataRequired, Length , InputRequired , AnyOf , EqualTo 
from ..database         import User , UserSchema
from uuid               import uuid4
from datetime           import datetime
from sqlalchemy         import and_
import os 

class AuthenRepository :
    def __init__(self, db) :
        self.db = db

    class modelFormLogin(FlaskForm):
        username = StringField('username',validators=[ InputRequired('username is Required!')]  , render_kw={"placeholder": "Enter username"} )
        password = PasswordField(
            'password',
            render_kw={"placeholder": "Enter password"})

    class modelFormRegister(FlaskForm):
        username        = StringField('username' , 
            validators  = [
                InputRequired( 'username is Required!'),
                Length(min = 3,max=8,message=('Username must between 3 and 8 character.')),
                ], 
            render_kw   = {"placeholder": "Enter username" } )
        
        password    = PasswordField(
            'password',
            validators=[Length(min = 3 , max=8, message=('Password must between 3 and 8 character.')), 
                        InputRequired('password is Required!'), 
                        EqualTo('confirm' , message='Password must match')],
            render_kw={"placeholder": "Enter password"})

        confirm = PasswordField(
            'repeat-password',
            validators=[ InputRequired( 'Comfirm password is Required!')],
            render_kw={"placeholder": "Confirm-Password"})
        
    def CheckDuplicateUser(self, username) : 
        try :
            object_user = User.query.filter( User.username == username).first()
            user_schema = UserSchema()
            json_user   = user_schema.dump(object_user)
            if json_user == {} :
                return "success"
            else :
                return "Username is Already Exist!"
        except Exception as e :
            raise Exception("CheckDuplicateUser : " + str(e))

    def insertUser(self , username , password) :
        try : 
            user_id = str(uuid4())[:16]
            user = User(user_id, username, password, datetime.now())
            self.db.session.add(user)
            self.db.session.commit()
        except Exception as e :
            raise Exception("insertUser Error : " + str(e))

    def verifyUser(self , username , password) : 
        try :
            user_obj    = User.query.filter(and_( User.username == username , User.password == password)).first()
            user_schema = UserSchema()
            user        = user_schema.dump(user_obj)
            if user == None or user == {} :
                return { "status" : "fail" , "data" : user }
            else :
                return { "status" : "success" , "data" : user }
        except Exception as e :
            raise Exception("verifyUser : " + str(e))
