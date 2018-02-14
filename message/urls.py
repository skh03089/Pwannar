# Created by Inseong on 2018-02-05
from django.urls import path
from . import views

app_name = 'message'

urlpatterns = [
    path('messages/', views.message_list, name='messages'),
    path('<int:pk>/', views.message_detail, name='message_detail'),
    path('delete/<int:pk>', views.delete_message, name='message_delete'),
    path('send/<str:username>', views.send_message, name='message_send'),
    path('send_messages/', views.send_message_list, name= 'send_messages'),
]