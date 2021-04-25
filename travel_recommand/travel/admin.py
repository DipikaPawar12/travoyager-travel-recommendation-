from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(User_Account)
admin.site.register(Destination)
admin.site.register(Place)


admin.site.register(Place_Review)
admin.site.register(Place_Image)
admin.site.register(User_Input)
admin.site.register(Itinerary)
admin.site.register(Hotel)

admin.site.register(Hotel_Booking)
admin.site.register(Transport)
admin.site.register(Transport_Booking)
admin.site.register(Taxi_Booking)
