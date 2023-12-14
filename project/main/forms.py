from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from main.models import Client,Post

# login,register forms
class ClientLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'name' : 'username',
        'placeholder' : 'Имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'name' : 'password',
        'placeholder' : 'Пароль'
    }))
    
    class Meta:
        model = Client
        fields = ['username','password']

class RegisterClientForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'name' : 'username',
        'placeholder' : 'Имя пользователя'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'name' : 'password1',
        'placeholder' : 'Пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'name' : 'password2',
        'placeholder' : 'Повторите пароль'
    }))
    email = forms.EmailField(
        max_length=254,
        help_text='Обязательное поле. Введите действительный email адрес.',
        widget=forms.EmailInput(attrs={'placeholder': 'Введите ваш email'})
    )
    avatar = forms.ImageField(required=False)
    
    class Meta:
        model = Client
        fields = ['username', 'email', 'password1', 'password2', 'avatar']
        
        
# edit post form
class EditCreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title','content','image')