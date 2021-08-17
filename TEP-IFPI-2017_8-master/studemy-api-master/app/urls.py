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
#from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls import include, url, handler400, handler403, handler404, handler500
from django.conf.urls.static import static
from django.urls import path
from core import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/courses/', views.PublicCourseList.as_view(), name=views.CourseList.name),
    path('api/buy-course/', views.buy_course, name='buy-course'),
    path('api/favorite-course/', views.favorite_course, name='favorite-course'),
    path('api/remove-course/', views.remove_course, name='remove-course'),
    path('api/get-myself/', views.CurrentUserView.as_view(), name='get-myself'),
    path('api/get-faturamento/', views.FaturamentoView.as_view(), name='get-faturamento'),
    
    path('api/created-courses/<int:pk>/', views.CourseDetail.as_view(), name=views.CourseDetail.name),
    path('api/created-courses/', views.CourseList.as_view(), name=views.CourseList.name),
    #DONE:    
    path('api/discountcoupons/', views.DiscountCouponList.as_view(), name=views.DiscountCouponList.name),
    path('api/discountcoupons/<int:pk>/', views.DiscountCouponDetail.as_view(), name=views.DiscountCouponDetail.name),

    path('api/students/', views.StudentList.as_view(), name=views.StudentList.name),
    path('api/students/<int:pk>/', views.StudentDetail.as_view(), name=views.StudentDetail.name),
    
    path('api/teachers/', views.TeacherList.as_view(), name=views.TeacherList.name),
    path('api/teachers/<int:pk>/', views.TeacherDetail.as_view(), name=views.TeacherDetail.name),
    
    path('api/subscriptions/', views.SubscriptionList.as_view(), name=views.SubscriptionList.name),
    path('api/subscriptions/<int:pk>/', views.SubscriptionDetail.as_view(), name=views.SubscriptionDetail.name),
    
    path('api/token-auth/', views.CustomAuthToken.as_view(), name='obtain-token'),
    path('api/password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/', views.ApiRoot.as_view(), name=views.ApiRoot.name),
]

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'
