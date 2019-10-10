from django.contrib.auth.models import User

from django.db import Q

class EmailAuthenticate(object):

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(email=username) | Q(username=username))
        except User.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            return User.objects.filter(email=username).order_by('id').first()

        if user.check_password(password):
            return user
        return None

    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None