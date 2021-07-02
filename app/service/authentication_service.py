from ..function import hashPassword

class AuthenService :
    def __init__(self, AuthenRepository):
        self.authen_repository = AuthenRepository

    def formLogin(self):
        return self.authen_repository.modelFormLogin()

    def formRegister(self):
        return self.authen_repository.modelFormRegister()

    def register(self , form):
        try :
            checkusername = self.authen_repository.CheckDuplicateUser(form.username.data)
            if checkusername == 'success' :
                hashpassword = hashPassword(password = form.password.data)
                self.authen_repository.insertUser( form.username.data , hashpassword)
                return 'success' # redirect to login 
            else :
                return checkusername
        except Exception as e :
            raise Exception("service_register : " + str(e))

    def verifyUser(self , form):
        try :
            password = hashPassword(password = form.password.data)
            return self.authen_repository.verifyUser(form.username.data , password)
        except Exception as e :
            raise Exception("service_verifyUser : " + str(e))
