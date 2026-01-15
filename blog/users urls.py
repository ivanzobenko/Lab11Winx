from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # регистрация нового пользователя
    path('register/', views.register, name='register'),
    # вход
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # выход
    path('logout/', auth_views.LogoutView.as_view(next_page='post_list'), name='logout'),
]
