from django.contrib import admin
from django.urls import path,include
from api.views import StudentView,UserLoginView
from api.views import LogOutView
from api.views import UserChangePasswordView
from api.views import UserSendPasswordResetView,ResetPasswordView

urlpatterns = [
    path('register/',StudentView.as_view() , name = 'student_view'),
    path('login/',UserLoginView.as_view(), name = 'login_view'),
    path('logout/',LogOutView.as_view(),name = 'Logout'),
    path('changepassword/',UserChangePasswordView.as_view() , name = 'Change_Password'),
    path('send-reset-password-view/',UserSendPasswordResetView.as_view(), name = 'Reset-Password'),
    path('user-password-reset-view/<uid>/<token>/',ResetPasswordView.as_view(), name = 'Reset_Password_with_Email')
]




