"""
URL configuration for AuthorityCenter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from users.views import jwt_login, get_code_verifier, UserList, UserDetails, UserTokenDetails

urlpatterns = [
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('admin/', admin.site.urls),
    path('jwt_login', jwt_login),
    path('get_code_verifier', get_code_verifier),
    path('users/', UserList.as_view()),
    path('users/<pk>/', UserDetails.as_view()),
    path('token/details/', UserTokenDetails.as_view()),
]
