from django.urls import path
from . import views

app_name = 'tokens'

urlpatterns = [
    path('', views.index, name='index'),
    path('print/<int:num>', views.print, name='print'),
    path('scanner/', views.scanner, name='scanner'),
]