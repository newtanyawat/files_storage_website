from flask import redirect , render_template ,render_template_string , session , redirect , request
import os 


class AuthenController:
    def __init__(self , Blueprint , AuthenService) :
        self.route = Blueprint('Authen', __name__)
        self.authenService = AuthenService
    
    def transportGateWay(self):
        self.route.add_url_rule('/',            'login',        self.login,     methods=['GET' , 'POST'])
        self.route.add_url_rule('/logout',      'logout',       self.logout,    methods=['GET'])
        self.route.add_url_rule('/register',    'register',     self.register,  methods=['GET' , 'POST'])
        return self.route

    def login(self):       
        try :
            errors  = False
            form    = self.authenService.formLogin()
            if request.args.get('error') :
                errors = '----- Please login First -----'
            if "user_login" in session :
                return redirect('/upload')
            elif request.method == "POST" and form.validate_on_submit() : 
                verifyUser = self.authenService.verifyUser(form)
                if verifyUser['status'] == 'success' :
                    session["user_login"] = { "user_id" : verifyUser['data']['user_id'] , "username" : form.username.data}
                    return redirect('/upload')
                elif verifyUser['status'] == 'fail' :
                    errors  =  'Username or Password Incorrect!'
            return render_template(os.path.join('user','login.html') , form = form , error = errors)
        except Exception as e :
            return "login error : " + str(e)
   
    def register(self):       
        try :
            errors = False
            form = self.authenService.formRegister()
            if "user_login" in session :
                return redirect('/upload')
            if form.validate_on_submit():
                register = self.authenService.register(form)
                if register == 'success' :
                    return redirect('/')
                else :
                    errors  =  f'{register}'
            return render_template(os.path.join('user','register.html') , form = form  , error = errors)
        except Exception as e :
            return "register error : " + str(e)

    def logout(self) :
        try :
            session.pop('user_login' , None)
            return redirect('/')
        except Exception as e :
            return 'logOut error : ' + str(e)
