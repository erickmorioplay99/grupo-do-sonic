from django.urls import path
from userprofile.views import userprofile_view, userprofile_register

urlpatterns = [
    path('', userprofile_view, name='userprofile_view'),
    path('register/', userprofile_register, name='userprofile_register_view')
]