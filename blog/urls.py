from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('comments/', include('comments.urls')),
    path('', include('posts.urls')),  # главная страница и посты
]