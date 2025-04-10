from django.urls import path
from . import views

app_name = 'device_connector'

urlpatterns = [
    path('devices/', views.device_list, name='device_list'),
    path('devices/connected/', views.connected_devices, name='connected_devices'),
    path('devices/scan/', views.scan_now, name='scan_now'),
] 