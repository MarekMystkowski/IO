import django.forms as froms

from django.contrib.auth.models import User

class UserForm(froms.ModelForm):
    password = froms.CharField(widget=froms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
