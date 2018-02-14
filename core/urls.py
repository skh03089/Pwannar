from django.urls import path
from core import views
from django.contrib import admin

app_name = 'core'

urlpatterns = [
    path('', views.MainPage, name='mainpage'),
    path('admin/', admin.site.urls),
    path('create/', views.board_create, name='board_create'),
    path('tag/<int:tag_pk>', views.board_list, name='board_list_by_tag'),
    path('<int:pk>/', views.board_detail, name='board_detail'),
    path('list/', views.board_list, name='board_list'),
    path('<int:pk>/update/', views.board_update, name='board_update'),
    path('<int:pk>/delete/', views.board_delete, name='board_delete'),
    path('<int:pk>/like/', views.article_like, name='article_like'),
]
