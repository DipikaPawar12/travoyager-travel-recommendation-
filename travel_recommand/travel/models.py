from django.db import models

# Create your models here.
class User(models.Model):
    user_id=models.IntegerField(primary_key=True,auto_created=True)
    username = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    contact = models.IntegerField()
    gender = models.CharField(max_length=1)
    dob = models.DateTimeField()

    def __str__(self):
        return self.user_id

 
class User_Account(models.Model):
    account_id=models.IntegerField(primary_key=True)
    user_id=models.ForeignKey(User,default=1,on_delete=models.SET_DEFAULT)
    acount_balance=models.FloatField()

    def __str__(self):
        return self.account_id

class Destination(models.Model):
    dest_id=models.IntegerField(primary_key=True)
    dest_name=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    temprature=models.FloatField()
    humidity=models.FloatField()

    def __str__(self):
        return self.dest_id     

class Place(models.Model):
    place_id=models.IntegerField(primary_key=True)
    dest_id=models.ForeignKey(Destination,default=1,on_delete=models.SET_DEFAULT)    
    name_place=models.CharField(max_length=100)
    desc_place=models.CharField(max_length=200)
    name_city=models.CharField(max_length=100)
    latitude=models.FloatField(unique=True)
    longitude=models.FloatField(unique=True)
    extra_charge=models.FloatField()
    image_place=models.ImageField(height_field=100,width_field=100)
    time_durationForVisit=models.TimeField()
    rate_place=models.FloatField()
    type_ofPlace=models.CharField(max_length=200)

    def __str__(self):
        return self.place_id          

class Place_Review(models.Model):
    place_id=models.ForeignKey(Place,default=1,on_delete=models.SET_DEFAULT,primary_key=True)
    user_id=models.ForeignKey(User,default=1,on_delete=models.SET_DEFAULT,primary_key=True)    
    review_place=models.TextField(max_length=1000,null=True)
    rate_place=models.TextField(max_length=2,null=True)

    def __str__(self):
        return self.place_id+self.user_id

class User_Input(models.Model):
    trip_id=models.IntegerField(primary_key=True)
    user_id=models.ForeignKey(User,default=1,on_delete=models.SET_DEFAULT)    
    dest_id=models.ForeignKey(Destination,default=1,on_delete=models.SET_DEFAULT)    
    location=models.CharField(max_length=100)
    starting_date=models.DateField()
    ending_date=models.DateField()
    age_group=models.CharField(max_length=10)
    no_ofPeople=models.IntegerField()
    budget=models.FloatField()
    visit_place=models.CharField(max_length=200)
    trans_toChoose=models.CharField(max_length=10)

    def __str__(self):
        return self.trip_id

class Hotel(models.Model):
    hotel_id=models.IntegerField(primary_key=True)
    hotel_name=models.CharField(max_length=200)
    dest_id=models.ForeignKey(Destination,default=1,on_delete=models.SET_DEFAULT)    
    type_ofRoom=models.CharField(max_length=20)
    stayCharge_dayPerRoom=models.FloatField()
    mealCharge_perPerson=models.FloatField()
    capacity=models.IntegerField(max_length=2)
    service=models.CharField(max_length=200)
    rate_hotel=models.TextField(max_length=2,null=True)
    image_hotel=models.ImageField(height_field=100,width_field=100)
    type_ofHotel=models.CharField(max_length=200)

    def __str__(self):
        return self.hotel_id

class Hotel_Booking(models.Model):
    trip_id=models.ForeignKey(User_Input,default=1,on_delete=models.SET_DEFAULT,primary_key=True)
    hotel_id=models.ForeignKey(Hotel,default=1,on_delete=models.SET_DEFAULT,primary_key=True)
    date_ofBooking_hotel=models.DateField()
    charge_hotel=models.FloatField()
    no_ofRoom=models.IntegerField(max_length=2)

    def __str__(self):
        return self.trip_id+self.hotel_id

class Itinerary(models.Model):
    trip_id=models.ForeignKey(User_Input,default=1,on_delete=models.SET_DEFAULT,primary_key=True)
    place_id=models.ForeignKey(Place,default=1,on_delete=models.SET_DEFAULT,primary_key=True)
    arrival_DnT=models.DateTimeField()
    departure_DnT=models.DateTimeField()

    def __str__(self):
        return self.trip_id+self.place_id

class Image(models.Model):
    image_id=models.IntegerField(primary_key=True)
    place_id=models.ForeignKey(Place,default=1,on_delete=models.SET_DEFAULT,primary_key=True)
    image_ofPlace=models.ImageField(height_field=100,width_field=100)

    def __str__(self):
        return self.image_id+self.place_id

class Transport(models.Model):
    trans_id=models.IntegerField(primary_key=True)
    driver_name=models.CharField(max_length=100)
    place_holdOnce=models.CharField(max_length=1)
    place_holdTwice=models.CharField(max_length=1)
    trans_contact=models.IntegerField()
    capacity_trans=models.IntegerField()
    charge_perPerson=models.FloatField()

    def __str__(self):
        return self.trans_id

class Transport_Booking(models.Model):
    trans_id=models.ForeignKey(Transport,default=1,on_delete=models.SET_DEFAULT,primary_key=True)
    trip_id=models.ForeignKey(User_Input,default=1,on_delete=models.SET_DEFAULT,primary_key=True)
    date_ofBooking_trans=models.DateField()
    start_dateOfTrans=models.DateField()
    end_dateOfTrans=models.DateField()
    source=models.CharField(max_length=200)
    type_ofTrans=models.CharField(max_length=10)
    no_ofPerson_onTrans=models.IntegerField(max_length=2)
    charge_ofTrans=models.FloatField()

    def __str__(self):
        return self.trip_id+self.trans_id

class Taxi_Booking(models.Model):
    trans_id=models.ForeignKey(Transport,default=1,on_delete=models.SET_DEFAULT,primary_key=True)
    trip_id=models.ForeignKey(User_Input,default=1,on_delete=models.SET_DEFAULT,primary_key=True)
    date_ofBooking_taxi=models.DateField()
    charge_ofTaxiRide=models.FloatField()

    def __str__(self):
        return self.trip_id+self.trans_id
