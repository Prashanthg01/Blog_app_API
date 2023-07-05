from django.contrib.auth.decorators import login_required
from dj_rest_auth.views import LoginView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, BlogPostSerializer
from .models import BlogPost
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import views as auth_views
from rest_framework import status

class CustomLoginView(LoginView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    
@api_view(['GET'])
@login_required
def custom_logout(request):
    logout(request)
    return Response()

@api_view(['GET'])
@login_required
def blog_post_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 5
    blog_posts = BlogPost.objects.all()
    result_page = paginator.paginate_queryset(blog_posts, request)
    serializer = BlogPostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
@login_required
def create_blog_post(request):
    data = request.data.copy()
    data['author'] = request.user.id
    serializer = BlogPostSerializer(data=data)
    if serializer.is_valid():
        blog_post = serializer.save()
        serialized_data = serializer.data
        serialized_data['author'] = blog_post.author.username
        return Response(serialized_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogPostUpdateAPIView(APIView):
    def put(self, request, pk):
        try:
            blog_post = BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            return Response({"error": "BlogPost not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogPostSerializer(blog_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)