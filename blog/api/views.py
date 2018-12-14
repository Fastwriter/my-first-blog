from django.contrib.auth.models import User
from blog.models import Post
from rest_framework import viewsets
from blog.api.serializers import UserSerializer, PostSerializer

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer