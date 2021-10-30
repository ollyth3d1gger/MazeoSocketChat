# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='chats'),
    #path('instructor/', views.instructorindex, name='instructorchat'),
    path('group/<str:course_id>/', views.room, name='room'),
    path('filemessage/', views.filemessage, name='filemessage'),

]