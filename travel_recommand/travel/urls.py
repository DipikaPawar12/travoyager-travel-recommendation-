from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^userRegister$', userRegister, name='userRegister'),
    url(r'^userInput$', userInput, name='userInput'),
    url(r'^userLogin$', userLogin, name='userLogin'),
    url(r'^split_userInput$', split_userInput, name='split_userInput'),
    url(r'^placeFetch$', placeFetch, name='placeFetch'),
    url(r'^temp$', temp, name='temp'),

]