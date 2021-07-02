from flask      import render_template
from datetime   import datetime , timedelta
from .server    import app
import pytz , hashlib , os
#! date_time Local = +0 Hr , Server = +7 Hr

def time():
    tz = pytz.timezone('Asia/Bangkok')
    timeNow = datetime.now(tz)
    # deltime = timeNow + timedelta(hours=int(-1))
    # print("deltime : " , deltime)
    # print("timeNow : " , timeNow)
    # print("compare : " , timeNow == deltime)
    return timeNow


def hashPassword(password):
    try : 
        salt = bytes(app.config['SECRET_KEY'], 'utf-8')
        password = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000).hex()
        return password
    except Exception as e :
        raise Exception("hashPassword : " + str(e))

def error_templates(e):
    try : 
        return render_template(os.path.join('files','error.html'), errors = e )
    except Exception as e :
        raise Exception("error_templates : " + str(e))

def datetimeCompare(datetimeformDB) :
    try :
        return datetime.strptime(datetimeformDB, '%Y-%m-%dT%X.%f') < datetime.now()
    except Exception as e :
        raise Exception("datetimeCompare : " + str(e))


