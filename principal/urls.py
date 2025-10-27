
from django.urls import path
from . import views

urlpatterns = [
    path('admin-home/',views.Adminhome,name='admin_home'),
    path('admindashboard/',views.Admindashboard,name='admin_dashboard'),
    path('adminaddstudent/',views.AdminAddStudent,name='admin_add_student'),
    path('adminaddcourse/',views.AdminAddCourse,name='admin_add_course'),


    path('admineditstudent/<int:id>',views.AdminEditStudent,name="admin_edit_student"),
    path('admindeletestudent/<int:id>',views.AdminDeleteStudent,name='admin_delete_student'),
    path('admineditdepartment/<int:id>',views.AdminEditDepartment,name='admin_edit_department'),
    path('admindeletedepartment/<int:id>',views.AdminDeleteDepartment,name='admin_delete_department'),


    path('addoncourse',views.AdminAddOnCourse,name='addoncourse'),
    path('editaddoncourse/<int:id>',views.AdminEditAddOnCourse,name='admin_edit_on_course'),
    path('deleteaddoncourse/<int:id>',views.AdminDeleteAddOnCourse,name='admin_delete_on_course'),

    path('approve_course/<int:purchase_id>/', views.approve_course, name='approve_course'),
    path('reject_course/<int:purchase_id>/', views.reject_course, name='reject_course'),




]