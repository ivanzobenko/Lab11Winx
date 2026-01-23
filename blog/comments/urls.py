from django.urls import path
from . import views
app_name = 'comments'
urlpatterns = [
    path('create/<int:post_id>/', views.comment_create, name='comment_create'),
    path('<int:pk>/edit/', views.comment_update, name='comment_update'),
    path('<int:pk>/delete/', views.comment_delete, name='comment_delete'),
]