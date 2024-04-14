from django.urls import path
import homeapp
import homeapp.views
from user import views

app_name = 'users'
urlpatterns = [
    path('users/profile/', views.UserAccountUpdateView.as_view()),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('', homeapp.views.home, name='homeapp'),
    path('logout/', views.logout_view, name='logout'),
]
