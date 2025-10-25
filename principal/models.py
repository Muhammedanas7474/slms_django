from django.db import models

# Create your models here.

class Department(models.Model):
    dept_name=models.CharField(max_length=10)
    dept_description=models.TextField()

    def __str__(self):
        return self.dept_name
    
class AddOnCourse(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    course_name=models.CharField(max_length=10)
    course_description=models.TextField()
    course_price=models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.course_name

