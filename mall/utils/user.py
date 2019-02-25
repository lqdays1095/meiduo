from django.contrib.auth.backends import ModelBackend
import re
from users.models import User
def get_user_by_account(account):
    try:
        if re.match(r'1[3-9]\d{9}', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except user.DoesNotExist:
        user = None
    return user
class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, requeset, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user is not None and user.check_password(password):
            return user
