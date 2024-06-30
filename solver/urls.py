# from unicodedata import name
# from django.views import View
from django.urls import path

from . import views

#UrlConf
urlpatterns = [
    path('', views.home, name='home'),
]

