from django.contrib import admin
from student.models import Student
from .models import Department  

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'dept', 'year_of_admission')
    search_fields = ('username', 'email')
    list_filter = ('dept', 'year_of_admission')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_name',)
