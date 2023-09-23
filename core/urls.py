"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="CTNAM API",
        default_version='v1.0',
        description="API pour l'application CTNAM ",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ismaelgrebo@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('common.urls')),
    path('api/quotidien/', include('membres.urls')),
    path('api/engagement/', include('engagements.urls')),
    path('api/finance/', include('finances.urls')),
    # API DOCUMENTATION
    path('doc', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    # FRONT
    path('', include('frontend.urls')),
] + static((settings.MEDIA_URL), document_root=(settings.MEDIA_ROOT))

