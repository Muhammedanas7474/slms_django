from django.db import models
from django.contrib.auth.models import AbstractUser
from principal.models import Department
from django.utils import timezone
from datetime import date
from principal.models import AddOnCourse

class Student(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    profile_pic = models.FileField(upload_to="profiles/", null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    year_of_admission = models.IntegerField(default=date.today().year)
    rollno=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f"{self.username} - {self.dept}"
    
class CoursePurchase(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(AddOnCourse, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.student.username} - {self.course.course_name}"
