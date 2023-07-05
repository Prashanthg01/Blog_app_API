from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('api/blogposts/', blog_post_list, name='blog_post_list'),
    path('api/blogposts/create/', views.create_blog_post, name='create_blog_post'),
]
