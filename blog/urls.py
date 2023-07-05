from django.urls import include, path
from blogapp.views import CustomLoginView, blog_post_list, create_blog_post, custom_logout, BlogPostUpdateAPIView
from dj_rest_auth.registration.views import RegisterView
from allauth.account.views import confirm_email
from blogapp import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/registration/', RegisterView.as_view(), name='account_registration'),
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/confirm-email/<str:key>/', confirm_email, name='account_confirm_email'),
    path('api/blogposts/', blog_post_list, name='blog_post_list'),
    path('api/blogposts/create/', views.create_blog_post, name='create_blog_post'),
    path('api/blogposts/update/<int:pk>/', BlogPostUpdateAPIView.as_view(), name='blogpost-update'),
]
