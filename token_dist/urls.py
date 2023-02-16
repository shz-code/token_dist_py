from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.auth.views import LoginView , LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', LoginView.as_view() , name='login'),
    # path('login/', LoginView.as_view(redirect_authenticated_user=True) , name='login'),
    path('logout/', LogoutView.as_view() , name='logout'),
    path('tokens/',include('tokens.urls', namespace='tokens')),
    path('event/<int:pk>',views.event, name="event_details"),
    path('event_update/',views.event_update, name="event_update"),
    path('delete_event/',views.delete_event, name="delete_event"),
    path('create_user/',views.create_user, name="create_user"),
    path('create_user_post/',views.create_user_post, name="create_user_post"),
]

urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)