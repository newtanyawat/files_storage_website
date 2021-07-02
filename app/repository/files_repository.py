from flask_wtf          import FlaskForm
from wtforms            import SelectField ,    PasswordField , SubmitField
from wtforms.validators import DataRequired,    Length
from flask_wtf.file     import FileField,       FileRequired
from werkzeug.utils     import secure_filename
from ..database         import Files , FileSchema
from datetime           import datetime , timedelta
from ..function         import hashPassword , datetimeCompare
from sqlalchemy         import update
import os

class filesRepository :
    def __init__(self , db) :
        self.db = db

    class uplaodForm(FlaskForm) :
        uploadfiles = FileField('files' , validators=[DataRequired()])
        password = PasswordField(
            'password',
            validators=[
                Length(max=8,message=('Password must less than 8 character.'))
            ])
        expire_duration = SelectField('Payload Type', coerce=int, validators=[DataRequired()] , 
        choices = [
            (1  , "1 minutes"),
            (5  , "5 minutes"),
            (60 , "1 hour"),
            (24 * 60 , "1 day"),
            (7  * 24 * 60 , "7 days")
            ])
        max_downloads = SelectField('Payload Type2', coerce=int, validators=[DataRequired()] ,
        choices = [
            (1, "1 download"),
            (2, "2 downloads"),
            (3, "3 downloads"),
            (4, "4 downloads"),
            (5, "5 downloads"),
            (20, "20 downloads"),
            (50, "50 downloads"),
            (100, "100 downloads"),
            ])
        files = SubmitField('files Uploaded', render_kw={"onclick": "test()"})
        signOut = SubmitField('Sign Out', render_kw={"onclick": "location.replace('/logout')"})

    class downloadForm(FlaskForm) :
        password = PasswordField(
            'password',)
        submitdownload = SubmitField('download')

    class deleteForm(FlaskForm) :
        password = PasswordField(
            'password',)
        submitdelete = SubmitField('delete')

    def saveFilelocal(self , file_id , form , typefile):
        form.uploadfiles.data.save(os.path.join('files',file_id+typefile))

    def saveFileDB(self , file_id , form , user_id) :
        try :
            create_date   = datetime.now()
            expire_date   = datetime.now()+ timedelta(minutes= form.expire_duration.data)
            file_data = Files(file_id        = file_id 
                            , user_id        = user_id 
                            , file_name      = form.uploadfiles.data.filename 
                            , file_password  = hashPassword(form.password.data) 
                            , create_date    = create_date 
                            , expire_date    = expire_date
                            , download_times = form.max_downloads.data)
            self.db.session.add(file_data)
            self.db.session.commit()
            return 'sueccess'
        except Exception as e :
            raise Exception("saveFileDB Error : " +str(e))

    def fileDetail(self , file_name : str):
        try :
            file_id , file_type = os.path.splitext(file_name)
            obj_files       = Files.query.filter( Files.file_id == file_id).first()
            files_schema    = FileSchema()
            json_files      = files_schema.dump(obj_files)
            return json_files
        except Exception as e:
            raise Exception("fileDetail Error : " +str(e))

    def reduceDownloadTime(self , file_id : str , download_times : int ):
        try :
            file_id , file_type = os.path.splitext(file_id)
            sql =   f'''
                    UPDATE files SET download_times = download_times -1 WHERE file_id = "{file_id}"
                    '''
            self.db.engine.execute(sql)
        except Exception as e:
            raise Exception("reduceDownloadTime Error : " +str(e))
   
    def removefileDB(self , file_id):
        try :
            file_id , file_type = os.path.splitext(file_id)
            sql =   f'''
                    DELETE FROM files WHERE file_id = "{file_id}"
                    '''
            self.db.engine.execute(sql)
        except Exception as e:
            raise Exception("reduceDownloadTime Error : " +str(e))

    def userUpload(self , user_id ):
        try :
            result = []
            files_schema    = FileSchema()
            obj_files       = Files.query.filter(Files.user_id == user_id).all()
            
            for data in obj_files :
                x = files_schema.dump(data)
                x['expire_date'] = datetime.strptime(x['expire_date'] , '%Y-%m-%dT%X.%f').strftime("%d/%m/%y %H:%M")
                file_id , file_type = os.path.splitext(x['file_name'])
                x['id'] = x['file_id'] + file_type
                result.append(x)
            return result #output emptry is {} 
        except Exception as e:
            raise Exception("userUpload Error : " +str(e))

    def time_delete_files():
        try :
            from ..database import db
            result = []
            files_schema    = FileSchema()
            obj_files       = Files.query.all()

            for data in obj_files :
                x = files_schema.dump(data)
                result.append(x)

            for data in result :
                file_name , file_type   = os.path.splitext(data['file_name'])
                file_id                 = data['file_id']
                local_file              = file_id+file_type
                if datetimeCompare(data['expire_date']) :
                    sql =   f'''
                            DELETE FROM files WHERE file_id = "{data['file_id']}" 
                            '''
                    db.engine.execute(sql)
                    path_file = os.path.join('files',local_file )
                    os.remove(path_file)
                else :
                    pass
        except Exception as e :
            raise Exception("time_delete_files Error" + str(e))


import threading ,time

class ThreadingExample:
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=60):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            filesRepository.time_delete_files()
            print('Doing something imporant in the background')

            time.sleep(self.interval)

example = ThreadingExample()
        
