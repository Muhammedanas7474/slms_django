from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegistrationForm,Loginform,StudentUpdateForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Student,CoursePurchase
from principal.models import AddOnCourse
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def Homepage(request):
    return render(request,'homepage.html') 


def Register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()  

            
            subject = "Welcome to College Portal"
            message = f"Hello {student.username},\n\nThank you for registering at our College Portal.\n\nYour account has been created successfully.\nYou can now log in and explore available courses.\n\nBest regards,\nCollege Admin"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [student.email]

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            except Exception as e:
                print("Email sending failed:", e)

            return redirect('login')  
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {"form": form})


def Login(request):
    if request.method == 'POST':
        form = Loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                if user.is_staff:
                    return redirect('admin_home')
                else:
                    return redirect('homepage')  
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = Loginform()

    return render(request, 'login.html', {'form': form})

@login_required(login_url="login")
def StudentDashboard(request):
    student = Student.objects.filter(username=request.user.username).first()
    courses = AddOnCourse.objects.all()
    
    purchased_courses = CoursePurchase.objects.filter(student=request.user)
    purchased_course_ids = purchased_courses.values_list('course_id', flat=True)

    return render(request, 'student_dashboard.html', {
        "student": student,
        "courses": courses,
        "purchased_courses": purchased_courses,
        "purchased_course_ids": purchased_course_ids,
    })



@login_required(login_url="login")
def StudentUpdate(request):
    student = request.user

    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')
    else:
        form = StudentUpdateForm(instance=student)

    return render(request, 'studentupdate.html', {"form": form})

def Logout(request):
    logout(request)
    return redirect("homepage")


@login_required(login_url="login")
def purchase_course(request, course_id):
    course = get_object_or_404(AddOnCourse, id=course_id)
    if not CoursePurchase.objects.filter(student=request.user, course=course).exists():
        CoursePurchase.objects.create(student=request.user, course=course)
    return redirect('student_dashboard')

@login_required(login_url="login")
def mark_course_complete(request, purchase_id):
    purchase = get_object_or_404(CoursePurchase, id=purchase_id, student=request.user)
    if purchase.status == "Approved":
        purchase.status = "Completed"
        purchase.save()
    return redirect('student_dashboard')

