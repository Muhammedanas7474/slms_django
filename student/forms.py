from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from .models import Student
from django.contrib.auth.forms import UserChangeForm


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "username", "email", "phone", "dob",
            "dept", "profile_pic", "age", "password"
        ]
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),  
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Student.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Student.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered. Please use another.")
        return email

    def save(self, commit=True):
        student = super().save(commit=False)
        
        student.password = make_password(self.cleaned_data['password'])
        if commit:
            student.save()
        return student

    
class Loginform(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))



class StudentUpdateForm(UserChangeForm):
    password = None  

    class Meta:
        model = Student
        fields = ['email', 'phone', 'dob', 'dept', 'profile_pic', 'age']
        widgets = {
            'dob': forms.DateInput(
                attrs={
                    'type': 'date',  
                    'class': 'form-control',  
                }
            ),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'dept': forms.Select(attrs={'class': 'form-select'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }