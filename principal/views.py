from django.shortcuts import render,redirect,get_object_or_404
from student.models import Student,CoursePurchase
from .models import Department,AddOnCourse
from django.contrib.auth.decorators import login_required
from .forms import AdminStudentForm,DepartmentForm,AdminEditForm,AdminAddOnCourseForm
from django.core.mail import send_mail
from django.conf import settings



# @login_required
def Adminhome(request):
    return render(request,'admin_base.html')



@login_required(login_url='login')
def Admindashboard(request):
    students=Student.objects.exclude(username__iexact="admin").order_by("rollno")
    departments=Department.objects.all()
    course=AddOnCourse.objects.all()
    purchased_course=CoursePurchase.objects.all()
    return render(request,'admin_dashboard.html',{"students":students,
                                                  "departments":departments,
                                                  "course":course,
                                                  "purchased_course":purchased_course})


def AdminAddStudent(request):
    if request.method == 'POST':
        form = AdminStudentForm(request.POST)
        if form.is_valid():
            student = form.save()  

            
            subject = "Welcome to College Portal"
            message = f"Hello {student.username},\n\nYour student account has been created successfully!\n\nUsername: {student.username}\nEmail: {student.email}\n\nPlease login to the portal."
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [student.email]

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            except Exception as e:
                print("Email failed:", e)

            return redirect('admin_dashboard')
    else:
        form = AdminStudentForm()
    
    return render(request, 'Adminaddstudent.html', {"form": form})


def AdminAddCourse(request):
    if request.method == 'POST':
        form=DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form=DepartmentForm()
    return render(request,'Adminaddcourse.html',{"form":form})


def AdminEditStudent(request,id):
    student=Student.objects.get(id=id)
    
    if request.method == 'POST':
        form=AdminEditForm(request.POST,instance=student)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form=AdminEditForm(instance=student)
    return render(request,'admin_edit_student.html',{"form":form})
        


def AdminDeleteStudent(request,id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('admin_dashboard')



def AdminEditDepartment(request,id):
    department = get_object_or_404(Department, id=id)

    if request.method == 'POST':
        form=DepartmentForm(request.POST,instance=department)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form=DepartmentForm(instance=department)
    return render(request,'admin_edit_department.html',{"form":form})




def AdminDeleteDepartment(request,id):
    department=get_object_or_404(Department,id=id)
    department.delete()
    return redirect('admin_dashboard')


def AdminAddOnCourse(request):
    form=AdminAddOnCourseForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form=AdminAddOnCourseForm()
    return render(request,'add_on_course.html',{"form":form})

def AdminEditAddOnCourse(request,id):
    course=get_object_or_404(AddOnCourse,id=id)
    if request.method == "POST":
        form=AdminAddOnCourseForm(request.POST,instance=course)
        if form.is_valid() :
            form.save()
            return redirect('admin_dashboard')
    else:
        form=AdminAddOnCourseForm(instance=course)
    return render(request,'edit_add_on_course.html',{"form":form})

def AdminDeleteAddOnCourse(request,id):
    course=get_object_or_404(AddOnCourse,id=id)
    course.delete()
    return redirect('admin_dashboard')



@login_required(login_url='login')
def approve_course(request, purchase_id):
    purchase = get_object_or_404(CoursePurchase, id=purchase_id)
    
    if purchase.status == "Pending":
        purchase.status = "Approved"
        purchase.save()
        
        
        student_email = purchase.student.email
        subject = "Course Approved"
        message = f"Hello {purchase.student.username},\n\nYour request to purchase the course '{purchase.course.course_name}' has been approved by the admin.\n\nYou can now access the course on your dashboard."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [student_email]
        
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        except Exception as e:
            print("Failed to send email:", e)
    
    return redirect('admin_dashboard')



@login_required(login_url='login')
def reject_course(request, purchase_id):
    purchase = get_object_or_404(CoursePurchase, id=purchase_id)
    if purchase.status == "Pending":
        purchase.status = "Rejected"
        purchase.save()
    return redirect('admin_dashboard')

    

    


