class UserManager(object):

    _users = {
        'izhar':{
            'password': 'password'
        }
    }

    def authenticate_user(self, login, password):
        if login in self._users:
            if self._users[login]['password'] == password:
                return True
        return False
