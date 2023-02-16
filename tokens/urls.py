from django.urls import path
from . import views

app_name = 'tokens'

urlpatterns = [
    path('event/<int:pk>', views.token, name='token_event'),
    path('print_token/<int:num>/<int:pk>', views.print_token, name='print_token'),
    path('generate_tokens/', views.generate_tokens, name='generate_tokens'),
    path('update_print_status/', views.update_print_status, name='update_print_status'),
    path('scanner/', views.scanner, name='scanner'),
]