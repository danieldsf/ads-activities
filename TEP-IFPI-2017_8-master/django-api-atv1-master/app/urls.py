"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls import include, url, handler400, handler403, handler404, handler500
from django.conf.urls.static import static
from django.urls import include, path
from core import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

urlpatterns = [
    path('', views.ApiRoot.as_view(), name='api-root'),
    path('reset-data', views.reset_data, name='reset-data'),
    path('profiles-total/', views.UserTotalList.as_view(), name=views.UserTotalList.name),
    path('upload/', views.FileView.as_view(), name='file-upload'),

    path('profiles', views.UserList.as_view(), name=views.UserList.name),
    path('profiles/<int:pk>/', views.UserDetail.as_view(), name=views.UserDetail.name),
    
    path('profile-posts', views.ProfilePostList.as_view(), name=views.ProfilePostList.name),
    path('profile-posts/<int:pk>', views.ProfilePostDetail.as_view(), name=views.ProfilePostDetail.name),

    path('posts', views.PostList.as_view(), name=views.PostList.name),
    path('posts/<int:pk>', views.PostDetail.as_view(), name=views.PostDetail.name),

    path('comments', views.CommentList.as_view(), name=views.CommentList.name),
    path('comments/<int:pk>', views.CommentDetail.as_view(), name=views.CommentDetail.name),

    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ROUTERS:

router = DefaultRouter()
router.register(r'profiles',views.UsersViewSet,base_name='profiles')

profiles_router = routers.NestedSimpleRouter(router, r'profiles', lookup='user')
profiles_router.register(r'posts',views.PostsViewSet)
posts_router = routers.NestedSimpleRouter(profiles_router, r'posts', lookup='post')
posts_router.register(r'comments',views.CommentsViewSet)

profiles_router = routers.NestedSimpleRouter(router, r'profiles', lookup='user')
profiles_router.register(r'posts',views.PostsViewSet)
posts_router = routers.NestedSimpleRouter(profiles_router, r'posts', lookup='post')
posts_router.register(r'comments',views.CommentsViewSet)

urlpatterns += profiles_router.urls
urlpatterns += posts_router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)