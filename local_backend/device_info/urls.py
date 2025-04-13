from django.urls import path
from . import views

app_name = 'device_info'

urlpatterns = [
    path('', views.device_info_list, name='device_info_list'),
    path('<str:device_id>/', views.device_info_detail, name='device_info_detail'),
] 