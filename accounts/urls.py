from django.urls import path
from accounts import views

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.Create_User, name='create_user'),
    path('signin/', views.SignIn, name='signin'),
    path('signout/', views.SignOut, name='signout'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
    path('myinfo/edit/', views.edit_myinfo, name='edit_myinfo'),
    path('profile/<str:username>/', views.myinfo, name='myinfo'),
    path('confirm/<str:username>/',views.confirm, name='confirm'),
    path('confirm/<str:username>/resend', views.resend, name='resend')
]
