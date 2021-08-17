import json, os
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
from django.db import transaction
from rest_framework import generics,viewsets,status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer   

    def get_queryset(self):
        try: 
            return Post.objects.filter(user=self.kwargs['user_pk'])
        except KeyError:
            return Post.objects.all()

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        try: 
            return Comment.objects.filter(post=self.kwargs['post_pk'])
        except KeyError:
            return Comment.objects.all()
### 

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'profile-list'
    http_method_names = ['get']

class UserPostList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-post-list'

class UserPostCommentList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-post-comment-list'

class UserTotalList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserTotalSerializer
    name = 'profile-total'
    http_method_names = ['get']

class ProfilePostList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfilePostSerializer
    name = 'profile-post-list'
    http_method_names = ['get']

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name = 'post-list'

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    name = 'comment-list'

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'profile-detail'
    http_method_names = ['get']

class UserPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-post-detail'

class UserPostCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-post-comment-detail'

class ProfilePostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfilePostSerializer
    name = 'profile-post-detail'
    http_method_names = ['get']

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerDetail
    name = 'post-detail'

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    name = 'comment-detail'

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({'profiles': reverse(UserList.name,request=request),
        'profile-total': reverse(UserTotalList.name,request=request),
        'profile-posts': reverse(ProfilePostList.name,request=request),
        'posts': reverse(PostList.name,request=request),
        'comments': reverse(CommentList.name,request=request),
        'reset-data': reverse('reset-data',request=request),})

@transaction.atomic
def reset_data(request):
    try:
        # Clearing previous data:
        Address.objects.all().delete() 
        User.objects.all().delete() 

        # Loading the file:
        file = open(os.path.join(settings.PROJECT_DIR, 'db.json'))
        read_file = json.dumps(file.read())
        file.close()
        file_content =  eval(json.loads(read_file))
        
        # Saving one by one:
        for user in file_content['users']:
          User.save_from_json(**user)

        for post in file_content['posts']:
          Post.save_from_json(**post)

        for comment in file_content['comments']:
          Comment.save_from_json(**comment)

        return JsonResponse({'error': False})
    except Exception as e:
        return JsonResponse({'error': str(e)})

# Fake

class FileView(APIView):    
    parser_classes = (MultiPartParser, FormParser)

    @File.fake_me
    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)