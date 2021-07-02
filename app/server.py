from flask import Flask
import os , logging
from flask_cors import CORS

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__ , static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'tanyawatsepsuk'

CORS(app, cors_allowed_origins="*")

# @app.after_request
# def after_request(response):
#     allow_origin_list = ["*"]
#     # allow_origin_list = ['http://localhost:8080',"'http://localhost:8081"]
#     if 'HTTP_ORIGIN' in request.environ and request.environ['HTTP_ORIGIN']  in allow_origin_list:
#         response.headers.add('Access-Control-Allow-Origin', request.environ['HTTP_ORIGIN'] )
#         response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With,Content-type,withCredentials,authorization')
#         response.headers.add('Access-Control-Allow-Methods', 'PUT,GET,POST,DELETE')
#     return response

# @app.after_request
# def after_request(response):
#     response.headers.add(
#     'Access-Control-Allow-Origin',
#     '*',
#     )
#     response.headers.add(
#     'Access-Control-Allow-Credentials',
#     'true'
#     )
#     response.headers.add(
#     'Access-Control-Allow-Headers',
#     'X-Requested-With,Content-type,withCredentials,authorization'
#     )
#     response.headers.add(
#     'Access-Control-Allow-Methods',
#     'GET,PUT,POST,DELETE,OPTIONS'
#     )
#     return response

