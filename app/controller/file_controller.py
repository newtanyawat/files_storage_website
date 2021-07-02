from flask          import redirect , render_template ,render_template_string , session , redirect , request ,send_from_directory
from uuid           import uuid4
from datetime       import datetime , timedelta
from ..function     import hashPassword , error_templates , datetimeCompare
import os

config = {"max_content" : 104857600 }

class FileController:
    def __init__(self , Blueprint , FileService) :
        self.route = Blueprint('Files', __name__)
        self.filesService = FileService
    
    def transportGateWay(self):
        self.route.add_url_rule('/upload',      'upload',       self.upload,        methods=['GET' , 'POST'])
        self.route.add_url_rule('/download',    'download',     self.download,      methods=['GET' , 'POST'])
        self.route.add_url_rule('/delete',      'delete',       self.delete,        methods=['GET' , 'POST'])
        self.route.add_url_rule('/link',        'link',         self.link,          methods=['GET' , 'POST'])
        return self.route

    def upload(self):
        try :
            #*intail value
            errors = False

            #*Check error
            if request.args.get('error') :
                errors = '----- Max Content files -----'


            #*Main function 
            if "user_login" in session :
                username = session['user_login']['username']
                form = self.filesService.uplaodForm()
                if form.validate_on_submit() and request.content_length > config["max_content"] :
                    return redirect("/upload?error=content")
                elif form.validate_on_submit(): 
                    file_id = self.filesService.uploadfile(form ,session['user_login']['user_id'] )
                    return redirect(f"/link?file_id={file_id}&file_name={form.uploadfiles.data.filename}&expire_date={form.expire_duration.data}") 
                return render_template(os.path.join('files','upload_form.html')
                                        , toolbar       = True
                                        , form          = form 
                                        , username      = username 
                                        , errors        = errors
                                        , table         = True
                                        , rows          = self.filesService.userUpload(session['user_login']['user_id']))
            else :
                return redirect("/?error=login")
        except Exception as e :
            return error_templates(e)

    def download(self):
        try :
            #*intail value
            errors ,  expire_time , expired   = False ,False,False 
            form        = self.filesService.downloadForm()
            file_id     = request.args.get('file_id')
            data_file   = self.filesService.dataFile(file_id)

            #*Link Download is Incorrect!
            if file_id == None or data_file == {} :
                return render_template(os.path.join('files','error.html'), errors = "Link Download is Incorrect!" )

            #*This file was expire by download times
            if data_file['download_times'] == 0 :
                expired  = True
                errors   = "This file was expire by download times"

            #*Expired by time
            if datetimeCompare(data_file['expire_date']) :
                expired  = True
                errors   = "This file Expired! at {0}".format(datetime.strptime(data_file['expire_date'] , '%Y-%m-%dT%X.%f'))

            #*Main function
            if data_file['download_times'] > 0 and form.validate_on_submit() : 
                if hashPassword(form.password.data)  == data_file['file_password'] : 
                    if self.filesService.checkfileExist(file_id) :
                        self.filesService.reduceDownloadTime( file_id ,data_file['download_times'])
                        return send_from_directory(os.path.join('../','files') , file_id , as_attachment=True, attachment_filename=data_file['file_name'] )
                    else :
                        expired  = True
                        errors =  'FILE WAS DELETE!'
                else : 
                    errors = "Password incorrect!"

            return render_template( os.path.join('files','download.html')  
                                    , file_name     = data_file['file_name']
                                    , file_id       = file_id
                                    , form          = form
                                    , errors        = errors
                                    , expired       = expired
                                    , expire_time   = expire_time
                                    , password      = False if data_file['file_password'] == "e759191b6d30475b92de6ef8fb716d8fa8be39f2192d71a99fbc027502619eda" else True )
        except Exception as e :
            return error_templates(e)

    def link(self):
        try :
            #*intail value
            expire_date = datetime.now() + timedelta( minutes= int(request.args.get('expire_date')))

            #*Main function
            return render_template(os.path.join('files','genlink.html') 
                                    , host          = request.host_url 
                                    , file_id       = request.args.get('file_id')
                                    , file_name     = request.args.get('file_name') 
                                    , expire_date   = expire_date.strftime('%A %x %H:%M' ))
        except Exception as e :
            return error_templates(e)

    def delete(self):
        try :            
            #*intail value
            errors      = False
            form        = self.filesService.deleteForm()
            file_id     = request.args.get('file_id')
            data_file   = self.filesService.dataFile(file_id)
            
            #*main function
            if "user_login" in session :
                user_id = session['user_login']['user_id']
                if form.validate_on_submit() : 
                    if session['user_login']['user_id'] == data_file['user_id'] :
                        if self.filesService.checkfileExist(file_id) :
                            path = os.path.join('files',file_id)
                            os.remove(path)
                            self.filesService.removefileDB(file_id)
                            return redirect('/')
                        else :
                            errors =  '---- FILE WAS DELETE! ----'
                    elif session['user_login']['user_id'] != data_file['user_id'] :
                        errors = "You need permission to perform this action!!"
            else :
                return redirect("/?error=login")
            return render_template( os.path.join('files','delete.html')  
                                    , file_name     = data_file['file_name']
                                    , file_id       = file_id
                                    , form          = form
                                    , errors        = errors
                                    , password      = False if data_file['file_password'] == "e759191b6d30475b92de6ef8fb716d8fa8be39f2192d71a99fbc027502619eda" else True )
        except Exception as e :
            return error_templates(e)