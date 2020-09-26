"""DjangoRestFramework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path, re_path
from firstRESTapi.views import (GetListObj, listapi, create, UpdateViews, detail, deletes,
                                listcreate, mixinlistCreate, retUpdDel, oneEndpoint,
                                formcheck, Authview, registerview, registerserview)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('form/', formcheck),
    path('list/', GetListObj.as_view()),
    path('listApi/', listapi.as_view()),
    path('create/', create.as_view()),
    path('Licreate/', listcreate.as_view()),
    path('register/', registerview.as_view()),
    path('registerserview/', registerserview.as_view()),
    path('auth/', Authview.as_view()),
    path('mix/', mixinlistCreate.as_view()),
    path('common/', oneEndpoint.as_view()),
    re_path(r'listApi/(?P<Title>\d+)/$', UpdateViews.as_view()),
    re_path(r'list/(?P<fun>\d+)/$', detail.as_view()),
    re_path(r'list/(?P<fun>\d+)/del/$', deletes.as_view()),
    re_path(r'comm/(?P<common>\d+)/$', retUpdDel.as_view()),
    path(r'api-token-auth/', obtain_jwt_token),
]
