from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from todo.models import Tasks


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="password",widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="confirm password",widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model=User
        fields=["username","email","password1","password2"]

        widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
    
    }


class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))    



class TodoForm(forms.ModelForm):
    class Meta:
        model=Tasks
        fields=["task_name"]
        widgets={
            'task_name':forms.TextInput(attrs={"class":"form-control"}),
        }

class TodoChangeForm(forms.ModelForm):
    class Meta:
        model=Tasks
        fields=["task_name","status"]  
        widgets={
        'task_name':forms.TextInput(attrs={"class":"form-control"}),
    }


class ForgotForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))    
    email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))  
    password1=forms.CharField(label="new Password",widget=forms.PasswordInput(attrs={"class":"form-control"})) 
    password2=forms.CharField(label="confirm new password ",widget=forms.PasswordInput(attrs={"class":"form-control"})) 