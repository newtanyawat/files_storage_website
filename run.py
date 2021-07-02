from flask          import Blueprint
from app.server     import app
from app.function   import time
from app.database   import db


from app.repository import authentication_repository,   files_repository 
from app.service    import authentication_service,      files_service
from app.controller import authentication_controller,   file_controller

authen_repository   = authentication_repository.AuthenRepository(db)
authen_service      = authentication_service.AuthenService(authen_repository)  
authen_controller   = authentication_controller.AuthenController(Blueprint, authen_service)

files_repository    = files_repository.filesRepository(db)
files_service       = files_service.FileService(files_repository)
file_controller     = file_controller.FileController(Blueprint, files_service)


app.register_blueprint(authen_controller.transportGateWay() , url_prefix="/" )
app.register_blueprint(file_controller.transportGateWay() , url_prefix="/" )

port = 3000
if __name__ == '__main__':
    print(f'Restart at : {time()} , server run at : http://localhost:{port}')
    app.run(host = '0.0.0.0' , debug= True , threaded=True,  port=port)
