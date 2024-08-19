from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import CustomUser


# class UserCreate(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = ('username', 'password1', 'password2', 'email', 'avatar')
#
#
# class UserChange(UserChangeForm):
#     class Meta(UserChangeForm.Meta):
#         model = CustomUser
#         fields = ('username', 'password', 'email', 'avatar')
#



class UserCreate(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'avatar')

class UserChange(UserChangeForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'avatar')
