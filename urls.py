"""mublog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from myapp.views import signup_view, login_view, feed_view, comment_view, like_view, post_view, logout_view
urlpatterns = [
    url(r'^$', signup_view, name='signup'),
    url(r'^login/$', login_view, name='login'),
    url(r'^post/$', post_view, name='post'),
    url(r'^feed/$', feed_view, name='feed'),
    url(r'^like/$', like_view, name='like'),
    url(r'^comment/$', comment_view, name='comment'),
    url(r'^logout/$', logout_view, name='logout'),
]
