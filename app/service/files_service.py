from uuid import uuid4
import os

class FileService :
    def __init__(self,filesRepository) :
        self.filesRepository = filesRepository  

    def uplaodForm(self):
            return self.filesRepository.uplaodForm()

    def downloadForm(self):
            return self.filesRepository.downloadForm()

    def deleteForm(self):
            return self.filesRepository.deleteForm()

    def uploadfile(self , form , user_id):
        try : 
            file_id     = str(uuid4())
            file_name , file_type = os.path.splitext(form.uploadfiles.data.filename)
            self.filesRepository.saveFilelocal(file_id , form , file_type)
            self.filesRepository.saveFileDB(file_id, form , user_id)
            return file_id+file_type
        except Exception as e :
            raise Exception("uploadfile Error : " + str(e))

    def checkfileExist(self , file_id):
        try :
            path_file = os.path.join('files',file_id)
            return os.path.exists(path_file)
        except Exception as e :
            raise Exception("checkfileExist Error : " + str(e))

    def dataFile(self , file_id) :
        try :
            return self.filesRepository.fileDetail(file_id)
        except Exception as e :
            raise Exception("dataFile Error : " + str(e))
    
    def reduceDownloadTime(self , file_id , download_times) :
        try :
            return self.filesRepository.reduceDownloadTime(file_id , download_times)
        except Exception as e :
            raise Exception("reduceDownloadTime Error : " + str(e))

    def userUpload(self , user_id) :
            return self.filesRepository.userUpload(user_id)
   
    def removefileDB(self , user_id) :
            return self.filesRepository.removefileDB(user_id)

    def ServiceTimeDeleteFile():
        print("ServiceTimeDeleteFile")
        