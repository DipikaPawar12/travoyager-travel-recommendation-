from django.conf.urls import url
from django.urls import path
from .views import *
import datetime

urlpatterns = [
    path('', index, name='index'),

    path('userRegister', userRegister, name='userRegister'),
    path('userLogin', userLogin, name='userLogin'),

    path('userInput', userInput, name='userInput'),
    path('split_userInput', split_userInput, name='split_userInput'),
    path('review/<int:pk>', review, name='review'),

    path('placeFetch', placeFetch, name='placeFetch'),
    path('temp', temp, name='temp'),
    path('temp/<int:pk>', tempBook, name='tempBook'),
    path('mapview', mapview, name='mapview'),
    path('tempDelete/<int:pk>', tempDelete, name='tempDelete'),
    path('placeExplore/<int:pk>/<int:location>', placeExplore, name='placeExplore'),
    path('addPlace/<int:counter>', addPlace, name='addPlace'),
    path('addPlace/addPlaceEntry/<int:pk>/<int:location>', addPlaceEntry, name='addPlaceEntry'),
    path('updatePlace/<int:pk>/<int:counter>', updatePlace, name='updatePlace'),

    path('bookHotel', bookHotel, name='bookHotel'),
    path('bookHotelOrNo', bookHotelOrNo, name='bookHotelOrNo'),
    path('bookHotelTable/<int:pk>', bookHotelTable, name='bookHotelTable'),
    path('alreadyBookedCon', alreadyBookedCon, name='alreadyBookedCon'),
    path('alreadyBooked/<int:trip>', alreadyBooked, name='alreadyBooked'),

    path('pay', pay, name='pay'),
    path('cancelBooking/<int:pk>', cancelBooking, name='cancelBooking'),
    path('cancelNorm', cancelNorm, name='cancelNorm'),
]