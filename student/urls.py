from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.Homepage,name='homepage'),
    path('register/',views.Register,name='register'),
    path('login/', views.Login, name='login'),
    path('logout/',views.Logout,name='logout'),
    path('dashboard/',views.StudentDashboard,name="student_dashboard"),
    path('studentupadte/',views.StudentUpdate,name='student_update'),

    
    path('purchase/<int:course_id>/', views.purchase_course, name='purchase_course'),
    path('complete/<int:purchase_id>/', views.mark_course_complete, name='mark_course_complete'),

    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'), 
         name='password_reset'),

    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
         name='password_reset_confirm'),

    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
         name='password_reset_complete'),
]

