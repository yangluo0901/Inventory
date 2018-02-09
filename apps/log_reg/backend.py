from django.contrib.auth.models import User
import bcrypt
class HashpwBackend(object):
    def authenticate(self,username = None, password = None):
        try:
            user =  User.objects.get(username = username)
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            user = User.objects.filter(username = username)[0]
        if bcrypt.checkpw(password.encode(),user.password.encode() ):
            return user
        return None
    def get_user(self, user_id):
        try:
            return User.objects.get(pk = user_id)
        except user.DoesNotExist:
            return None
