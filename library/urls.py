"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.template.defaulttags import url
from django.urls import path, include
from book import urls as book_urls
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from book.views import RegisterAPI


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(book_urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterAPI.as_view()),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/schema/', get_schema_view(title='library', description='This is the documentation of library api'),
         name='api_schema'),

    path('api/ui', TemplateView.as_view(
        template_name='docs.html',
        extra_context={'schema_url':'api_schema'}
        ), name='swagger-ui'),

]
