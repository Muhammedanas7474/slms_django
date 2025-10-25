from django import forms
from student.models import Student
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import Department,AddOnCourse

class AdminStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "rollno","username", "email", "phone", "dob",
            "dept", "age", "password"
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
    
class DepartmentForm(forms.ModelForm):
    class Meta:
        model=Department
        fields = "__all__"

class AdminEditForm(forms.ModelForm):
    class Meta:
        model=Student
        fields = [
            "rollno", "dept",  
        ]

class AdminAddOnCourseForm(forms.ModelForm):
    class Meta:
        model=AddOnCourse
        fields= [
            "course_name","course_description","course_price"
        ]

