from rest_framework_swagger.views import get_swagger_view
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path
from rest_framework_jwt.views import *
from core.views import ApiRoot

schema_view = get_swagger_view(title='Restaurapp API')

urlpatterns = [
    path('', ApiRoot.as_view(), name=ApiRoot.name),
    path('api/', include('core.urls')),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/oauth/', include('rest_framework_social_oauth2.urls')),
    path('api/jwt/token/get', obtain_jwt_token),
    path('api/jwt/token/refresh', refresh_jwt_token),
    path('api/jwt/token/verify', verify_jwt_token),
    path('api/docs', schema_view),

    path('admin/', admin.site.urls)
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
