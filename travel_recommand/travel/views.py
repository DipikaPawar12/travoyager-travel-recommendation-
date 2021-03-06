from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from datetime import datetime,timedelta, date
from django.db.models import Q

# Create your views here.
userId_glob=-1
def login(id):
    global  userId_glob
    userId_glob=id

def logout():
    global  userId_glob
    userId_glob=-1

def index(request):
    return render(request, 'index.html')


def userRegister(request): #register page
    logout()
    if request.method == 'POST': #if tap on submit button
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        email = request.POST.get('mail')
        contact = request.POST.get('contact')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        
        if cpassword == password: #check confirm password with password
            if(gender=='Male'): #convert into single char
                gender='M'
            elif(gender=='Female'):
                gender='F'
            else:
                gender='O'
            
            user = User(username=username, password=password,                        #Query to store user info
                        email=email, contact=contact, gender=gender, dob=dob)
            try:  
                user.save()
                user_obj = User.objects.get(username=username)
                login(user_obj.id)
                account = User_Account(user_id=user_obj, account_balance=50000)
                account.save()
               # return HttpResponseRedirect('/userInput') #after successfully submitted User can give response in User Input page
                return HttpResponseRedirect('/home')
            except Exception as e:
                print(e)
                errors = "*We found the same username or email id in our data. These should be unique. Try some new" #throw Exception if same data is found
                context = {                   
                    'username': username,
                    'mail': email,
                    'contact': contact,
                    'gender': gender,
                    'errors': errors,
                    'dob': dob,
                } #stay this details as user entered ,not removing everything
                return render(request, 'userRegister.html', context) #otherwise User Register HTML displays
        else:
            errors = "*Both the passwords are not matching. Try again" #both passwords aren't match
            context = {
                    'username': username,
                    'mail': email,
                    'contact': contact,
                    'gender': gender,
                    'errors': errors,
                    'dob': dob,
            } #stay this details as user entered ,not removing everything
            return render(request, 'userRegister.html', context) #otherwise User Register HTML displays
           
    else:
        return render(request, 'userRegister.html')#otherwise diplays SignUp HTML page
    

def userLogin(request):
    logout()
    if request.method == "POST": # If Got response from Login Form
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Try fetch data from table with same username
            user_obj = User.objects.get(username=username)
        except:
            # Username not Found!!
            user_obj = None
        
        if user_obj is None:
            error = "*Username you entered doesn't exist"
            return render(request, "userLogin.html", {"errors": error}) #Username doesn't exist
        elif not user_obj.password == password:
            errors = "*Invalid password"
            return render(request, "userLogin.html", {"errors": errors, "username": username})  #Password doesn't match
        else:
            login(user_obj.id)
            return HttpResponseRedirect('/home')
            
    return render(request, 'userLogin.html') #otherwise diplays Log IN HTML page

src_name_glob=""
desti_name_glob=""

def home(request):
    return render(request, 'home.html')

def aboutus(request):
    return render(request, 'aboutus.html')

def aboutteam(request):
    return render(request, 'aboutteam.html')

def profile(request):
    if userId_glob!=-1:
        user_obj = User.objects.get(id=userId_glob)
        acc_obj = User_Account.objects.get(user_id=user_obj)
        return render(request, 'profile.html',context={"user_obj" : user_obj, "acc_obj" : acc_obj})
    else:
        return HttpResponseRedirect('/userLogin')
   

def tripHistory(request):
 if userId_glob!=-1:
    user_obj = User.objects.get(id=userId_glob)
    try:
        user_in_obj = User_Input.objects.filter(user_id=user_obj).all()
    except:
        user_in_obj = None
    error = ""
    if user_in_obj == None or len(user_in_obj) == 0:
        error = "No Trip History"
    return render(request, "tripHistory.html", {"user_obj": user_in_obj, "error":error})
 else:
    return HttpResponseRedirect('/userLogin')
   
def userInput(request):
    if userId_glob!=-1:
        try:
            dest_available_obj = Destination.objects.all().order_by('dest_name')
        except:
            dest_available_obj = None

        user_obj = User.objects.get(id=userId_glob)

        user_in_obj = User_Input.objects.filter(user_id=user_obj).all()

        today = date.today()
        print(user_in_obj)
        for obj in user_in_obj:
            if obj.starting_date < today and obj.status=='Booked':
                print(obj.status)
                obj.status="completed"
                obj.save()
            elif obj.starting_date < today and obj.status=='ongoing':
                iti_onj = Itinerary.objects.filter(trip_id=obj).all()
                for obj1 in iti_onj:
                    obj1.delete()
                try: 
                    hotel_obj = Hotel_Booking.objects.get(trip_id=obj)
                    hotel_obj.delete()
                except:
                    pass
                obj.delete()
        
        try:
            user_in_obj = User_Input.objects.get(Q(status='ongoing') ,user_id=user_obj)
        except:
            user_in_obj=None

        if user_in_obj != None:
            return HttpResponseRedirect('/temp') 


        if dest_available_obj!=None:
            if request.method == "POST": # If Got response from Login Form
                src_name = request.POST.get('src_name')
                dest_name = request.POST.get('dest_name')
                if src_name==dest_name:
                    error="*Please enter differrent values"
                    return render(request, "userInput.html", {"dest_available_obj": dest_available_obj, "error":error})
                else:
                    global src_name_glob
                    global desti_name_glob
                    src_name_glob=src_name
                    desti_name_glob=dest_name
                    return HttpResponseRedirect('/split_userInput')
            return render(request, "userInput.html", {"dest_available_obj": dest_available_obj, "user_obj": user_in_obj})
        return render(request, 'userInput.html') #after successfully submitted User can give response in User Input page
    else:
        return HttpResponseRedirect('/userLogin')

def split_userInput(request):
    if userId_glob!=-1:
        today = (datetime.today()+timedelta(days=1)).strftime('%Y-%m-%d')
        context={
            'date': today
        }
        if request.method == "POST": # If Got response from Login Form
            starting_date = request.POST.get('starting_date')
            ending_date = request.POST.get('ending_date')
            no_of_adult = request.POST.get('no_of_adult')
            no_of_child = request.POST.get('no_of_child')
            budget = request.POST.get('budget')
            
            visit_place_type=''
            trans_to_choose = request.POST.get('trans_to_choose')

            beach = request.POST.get('beach')
            shopping = request.POST.get('shopping')
            historical = request.POST.get('historical')
            tracking = request.POST.get('tracking')
            religious = request.POST.get('religious')
            relaxing = request.POST.get('relaxing')
            
            if beach!=None:
                visit_place_type+='beach'
            if shopping!=None:
                visit_place_type+=',shopping'
            if historical!=None:
                visit_place_type+=',historical'
            if tracking!=None:
                visit_place_type+=',tracking'
            if religious!=None:
                visit_place_type+=',religious'
            if relaxing!=None:
                visit_place_type+=',relaxing'

            
            src_obj = Destination.objects.get(dest_name= src_name_glob)
            dest_obj = Destination.objects.get(dest_name= desti_name_glob)
            user_obj = User.objects.get(id=userId_glob)
            user_entry = User_Input(user_id=  user_obj ,dest_id= dest_obj,starting_date=starting_date ,source_id= src_obj, ending_date=ending_date
                                    ,no_of_adult = no_of_adult, no_of_child=no_of_child ,
                                    budget= budget ,   visit_place_type=visit_place_type , trans_to_choose=trans_to_choose, status='ongoing')
            try:  
                user_entry.save()
                print('success')
                return HttpResponseRedirect('/placeFetch')#after successfully submitted User can give response in User Input page
            except Exception as e:
                #context.append('error':e)
                return render(request, 'split_userInput.html', context)

        return render(request, 'split_userInput.html', context) #after successfully submitted User can give response in User Input page
    else:
        return HttpResponseRedirect('/userLogin')

def review(request, pk):
    if userId_glob!=-1:
        user_obj = User.objects.get(id=userId_glob)
        user_in_obj = User_Input.objects.get(trip_id=pk)

        itinary_gen = Itinerary.objects.filter(trip_id=user_in_obj).all()

        place_obj=[]
        review_status=[]
        for obj in itinary_gen:
            if obj.place_id not in place_obj:
                place_obj.append(obj.place_id)
                try:
                    review_obj = Place_Review.objects.get(user_id=user_obj, place_id=obj.place_id)
                except:
                    review_obj = None

                if review_obj==None :
                    review_status.append("remain")
                else:
                    review_status.append('done')

        common = zip(place_obj, review_status)

        if request.method == "POST": # If Got response from Review Form
            review = request.POST.get('review')
            rating = request.POST.get('rating')
            id = request.POST.get('placeId')

            place_objj = Place.objects.get(place_id=(int)(id))
            rate=place_objj.rate_place
            place_objj.rate_place=((float)(rating)+rate)/2
            
            rev_obj=Place_Review(user_id=user_obj, place_id=place_objj, review_place=review, rate_place=((float)(rating)+rate)/2)
            rev_obj.save()
            place_objj.save()
            return HttpResponseRedirect('/review/'+(str)(pk))
        return render(request,'reviewTrip.html',{"common": common})
    else:
        return HttpResponseRedirect('/userLogin')

def placeFetch(request):
    #print(userId_glob)
    if userId_glob!=-1:
        try:
            user_obj = User.objects.get(id=userId_glob)
            user_in_obj = User_Input.objects.get(Q(status='ongoing') ,user_id=user_obj)   
        except:
            user_in_obj=None
        
        if user_in_obj!=None:
            #dest_obj = Destination.objects.get(dest_id = user_in_obj.dest_id)
            choice = user_in_obj.visit_place_type
            choice=choice.split(',')
            place_obj = Place.objects.filter(type_of_Place__in = choice, dest_id=user_in_obj.dest_id).all().order_by('-extra_charge','rate_place','time_durationForVisit')
            print(len(place_obj))
            
            delta = user_in_obj.ending_date - user_in_obj.starting_date
            no_of_day_visit = delta.days+1

            given_date = user_in_obj.starting_date
            i=0
            k=0
            while i<(3*no_of_day_visit):
                place_obj_current = place_obj[k]
                k+=1

                if(i%3==0 and i!=0):
                    given_date+= timedelta(days=1)
                if(i%3==0):
                    t1 =  datetime.strptime('09:30:00', '%H:%M:%S')
                    t2 =  datetime.strptime('12:30:00', '%H:%M:%S')
                elif(i%3==1):
                    t1 =  datetime.strptime('14:30:00', '%H:%M:%S')
                    t2 =  datetime.strptime('17:30:00', '%H:%M:%S')
                elif(i%3==2):
                    t1 =  datetime.strptime('18:30:00', '%H:%M:%S')
                    t2 =  datetime.strptime('21:30:00', '%H:%M:%S')
                    

                slot1 = datetime.combine(given_date, datetime.time(t1))
                slot2 = datetime.combine(given_date, datetime.time(t2))
                print(slot1,' ',slot2)
                itinerary_gen = Itinerary(trip_id = user_in_obj, place_id = place_obj_current,arrival_DnT = slot1, departure_DnT = slot2)
                itinerary_gen.save()
                if(k>=len(place_obj) or (i==3*no_of_day_visit-1)):
                    break
                if(place_obj_current.time_durationForVisit.hour>3):
                    if(i%3==0):
                        slot1 = slot1.replace(hour=(14))
                        slot2 = slot2.replace(hour=(17))
                    elif(i%3==1):
                        slot1 = slot1.replace(hour=(18))
                        slot2 = slot2.replace(hour=(21))
                    elif(i%3==2):
                        slot1 = slot1.replace(hour=(9))
                        slot2 = slot2.replace(hour=(12))
                        slot1 += timedelta(days=1)
                        slot2 += timedelta(days=1)
                    i+=1

                    given_date = (slot2.date())

                    print(slot1,' ',slot2)
                    print(i)
                    itinerary_gen = Itinerary(trip_id = user_in_obj, place_id = place_obj_current,arrival_DnT = slot1, departure_DnT = slot2)
                    itinerary_gen.save()
                i+=1
            #itinary_gen = Itinerary.objects.filter(trip_id=user_in_obj).all()
            context={
                'itinary_gen': itinerary_gen
            }
            return HttpResponseRedirect('/temp')

        else:
            return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect('/userLogin')


def itinaryShow(curr_slot, itinary_gen, user_in_obj,  next_slot, current_date):
    dictionary={}
    t = datetime.strptime(curr_slot, '%H:%M:%S')
    curr_slot = datetime.combine(current_date, datetime.time(t))
    t = datetime.strptime(next_slot, '%H:%M:%S')
    curr_slot_end = datetime.combine(current_date, datetime.time(t))
    image_obj = Place_Image.objects.all()

    try:
        check = Itinerary.objects.filter(trip_id=user_in_obj, arrival_DnT=curr_slot).all()
    except:
        pass
    dictionary['trip_id'] = user_in_obj
    dictionary['arrival_DnT']= curr_slot
    dictionary['departure_DnT'] = curr_slot_end
    if len(check)>0:
        dictionary['arrival_DnT']= check[0].arrival_DnT
        dictionary['departure_DnT'] = check[0].departure_DnT
        dictionary['place_id'] = check[0].place_id
        for img in image_obj:
            if dictionary['place_id'].place_id == img.place_id.place_id:
                dictionary['img'] = (img.image_of_place)
                break       
        return (dictionary)

    dictionary['place_id'] = None
    dictionary['img']=None
    return (dictionary)

def temp(request):
    if userId_glob!=-1:
        user_obj = User.objects.get(id=userId_glob)
        user_in_obj = User_Input.objects.get(Q(status='ongoing') ,user_id=user_obj)


        delta = user_in_obj.ending_date - user_in_obj.starting_date
        no_of_day_visit = delta.days+1
        current_date = user_in_obj.starting_date

        itinary_gen = Itinerary.objects.filter(trip_id=user_in_obj).all()
        itinary = []
        for i in range(no_of_day_visit):
            itinary.append(itinaryShow('09:30:00', itinary_gen, user_in_obj, '12:30:00', current_date))
            itinary.append(itinaryShow('14:30:00', itinary_gen, user_in_obj, '17:30:00', current_date))
            itinary.append(itinaryShow('18:30:00', itinary_gen, user_in_obj, '21:30:00', current_date))
            current_date += timedelta(days=1)

        
        context={
            'itinary_gen': itinary,
            'org_iti': itinary_gen
        }
        return render(request,'temp.html', context)
    else:
        return HttpResponseRedirect('/userLogin')

def tempBook(request,pk):
    if userId_glob!=-1:
        user_obj = User.objects.get(id=userId_glob)
        user_in_obj = User_Input.objects.get(trip_id=pk)

        delta = user_in_obj.ending_date - user_in_obj.starting_date
        no_of_day_visit = delta.days+1
        current_date = user_in_obj.starting_date

        itinary_gen = Itinerary.objects.filter(trip_id=user_in_obj).all()
        itinary = []
        print(itinary)
        for i in range(no_of_day_visit):
            itinary.append(itinaryShow('09:30:00', itinary_gen, user_in_obj, '12:30:00', current_date))
            itinary.append(itinaryShow('14:30:00', itinary_gen, user_in_obj, '17:30:00', current_date))
            itinary.append(itinaryShow('18:30:00', itinary_gen, user_in_obj, '21:30:00', current_date))
            current_date += timedelta(days=1)

        context={
            'itinary_gen': itinary,
            'org_iti': itinary_gen,
            'not': 'No',
            'trip': user_in_obj.trip_id
        }
        return render(request,'temp.html', context)
    else:
        return HttpResponseRedirect('/userLogin')

def placeExplore(request, pk, location):
    place_obj = Place.objects.get(place_id=pk)
    place_img = Place_Image.objects.filter(place_id=place_obj).all()
    place_review = Place_Review.objects.filter(place_id=place_obj).all()
    context={
        'place_obj':place_obj,
        'place_img':place_img,
        'place_review':place_review,
        'location':location
    }
    return render(request, 'placeExplore.html', context)

def tempDelete(request, pk):
    iti_obj = Itinerary.objects.get(id=pk).delete()

    return HttpResponseRedirect('/temp')


def addPlace(request, counter):
    if userId_glob!=-1:
        limit=""
        user_obj = User.objects.get(id=userId_glob)
        user_in_obj = User_Input.objects.get(Q(status='ongoing') ,user_id=user_obj)

        delta = user_in_obj.ending_date - user_in_obj.starting_date
        no_of_day_visit = delta.days+1
        current_date = user_in_obj.starting_date
        
        itinary_obj = Itinerary.objects.filter(trip_id=user_in_obj).all()
        place =[]
        for obj in itinary_obj:
            place.append(obj.place_id.place_id)
        place_obj = Place.objects.filter(~Q(place_id__in = place), dest_id=user_in_obj.dest_id).all()
        if len(place_obj)==0:
            limit="All places are covered still you wish!!!"
            place_obj = Place.objects.filter(dest_id=user_in_obj.dest_id).all()
        image_obj = Place_Image.objects.all()
        img_list=[]
        for obj in place_obj:
            for img in image_obj:
                if obj.place_id == img.place_id.place_id:
                    img_list.append(img.image_of_place)
                    break

        common = zip(place_obj, img_list)
        context={
            'place_obj': common,
            'location': counter,
            'limit': limit
        }
        return render(request,'addPlace.html', context)
    else:
        return HttpResponseRedirect('/userLogin')

def addPlaceEntry(request, pk, location):
    if userId_glob!=-1:
        location-=1
        user_obj = User.objects.get(id=userId_glob)
        user_in_obj = User_Input.objects.get(Q(status='ongoing') ,user_id=user_obj)

        current_date = user_in_obj.starting_date + timedelta(days=(int)(location/3))    
        
        if(location%3==0):
            t1 =  datetime.strptime('09:30:00', '%H:%M:%S')
            t2 =  datetime.strptime('12:30:00', '%H:%M:%S')
        elif(location%3==1):
            t1 =  datetime.strptime('14:30:00', '%H:%M:%S')
            t2 =  datetime.strptime('17:30:00', '%H:%M:%S')
        else:
            t1 =  datetime.strptime('18:30:00', '%H:%M:%S')
            t2 =  datetime.strptime('21:30:00', '%H:%M:%S')

        slot1 = datetime.combine(current_date, datetime.time(t1))
        slot2 = datetime.combine(current_date, datetime.time(t2))

        place_obj = Place.objects.get(place_id = pk)
        itinerary_gen = Itinerary(trip_id = user_in_obj, place_id = place_obj,arrival_DnT = slot1, departure_DnT = slot2)
        itinerary_gen.save()
    
        return HttpResponseRedirect('/temp')
    else:
        return HttpResponseRedirect('/userLogin')

def updatePlace(request, pk, counter):
    if userId_glob!=-1:
        iti_obj = Itinerary.objects.get(id=pk).delete()
        return HttpResponseRedirect('/addPlace/'+str(counter))
    else:
        return HttpResponseRedirect('/userLogin')


def mapview(request):
    if userId_glob!=-1:
        user_obj = User.objects.get(id=userId_glob)
        user_in_obj = User_Input.objects.get(Q(status='ongoing') ,user_id=user_obj)

        today = datetime.today()
        print(today)
        itinary_gen = Itinerary.objects.filter(trip_id=user_in_obj, arrival_DnT__gt = today).all()

        context={
            'iti': itinary_gen
        }
        return render(request,'map.html', context)
    else:
        return HttpResponseRedirect('/userLogin')



def bookHotel(request):
    if userId_glob!=-1:
        user_obj = User.objects.get(id=userId_glob)
        user_in_obj = User_Input.objects.get(Q(status='ongoing') ,user_id=user_obj)

        obj = Hotel_Booking.objects.filter(trip_id = user_in_obj).all()
        if(len(obj)>0):
            return HttpResponseRedirect('/alreadyBooked/'+str(user_in_obj.trip_id))


        hotel_obj = Hotel.objects.filter(dest_id = user_in_obj.dest_id).all()
        
        for obj in hotel_obj:
            book_obj = Hotel_Booking.objects.filter(hotel_id = obj, payment='done', date_of_booking_hotel = user_in_obj.starting_date, ending_date=user_in_obj.ending_date).all()
            c=0
            tp=0
        
            for room in book_obj:
                c+=room.no_of_room

            if c>=obj.hotel_capacity:
                obj.delete()
                #dict_hotel.append(obj)

        context={
            'hotel_list':hotel_obj
        }
        return render(request, 'bookHotel.html', context)
    else:
        return HttpResponseRedirect('/userLogin')

def bookHotelTable(request, pk):
    if userId_glob!=-1:
        user_obj = User.objects.get(id=userId_glob)
        user_in_obj = User_Input.objects.get(Q(status='ongoing') ,user_id=user_obj)

        delta = user_in_obj.ending_date - user_in_obj.starting_date
        no_of_day_visit = delta.days+1

        total = user_in_obj.no_of_adult+user_in_obj.no_of_child
        hotel = Hotel.objects.get(hotel_id=pk)

        no_of_room_needed = (int)(total/hotel.capacity)+1
        charges =(int) (no_of_room_needed*hotel.stayCharge_dayPerRoom+hotel.mealCharge_perPerson*total)
        print(no_of_room_needed)
        print(hotel.stayCharge_dayPerRoom)
        print(hotel.mealCharge_perPerson)
        charges*=no_of_day_visit
        obj = Hotel_Booking(trip_id=user_in_obj, hotel_id = hotel, date_of_booking_hotel = user_in_obj.starting_date, 
                    ending_date = user_in_obj.ending_date,charge_hotel=charges, no_of_room = no_of_room_needed, payment='Remain')
        obj.save()
        return HttpResponseRedirect('/alreadyBookedCon')
    else:
        return HttpResponseRedirect('/userLogin')

def alreadyBooked(request, trip):
    if userId_glob!=-1:
        user_obj = User.objects.get(id=userId_glob)
        user_in_obj = User_Input.objects.get(trip_id = trip)
        hotel=Hotel_Booking.objects.get(trip_id = user_in_obj)
        context={
            'obj': hotel
        }
        return render(request,'alreadyBooked.html', context)
    else:
        return HttpResponseRedirect('/userLogin')

def alreadyBookedCon(request):
    if userId_glob!=-1:
        user_obj = User.objects.get(id=userId_glob)
        user_in_obj = User_Input.objects.get(Q(status='ongoing') ,user_id=user_obj)
        hotel=Hotel_Booking.objects.get(trip_id = user_in_obj)
        context={
            'obj': hotel
        }
        return render(request,'alreadyBooked.html', context)
    else:
        return HttpResponseRedirect('/userLogin')

def cancelNorm(request):
    if userId_glob!=-1:
        user_obj = User.objects.get(id=userId_glob)
        user_in_obj = User_Input.objects.get(Q(status='ongoing') ,user_id=user_obj)
        try:
            hotel=Hotel_Booking.objects.get(trip_id = user_in_obj, payment="Remain")
        except:
            hotel=None

        if hotel!=None:
            hotel.delete()
            
        return HttpResponseRedirect('/bookHotel')
    else:
        return HttpResponseRedirect('/userLogin')

def pay(request):
    if userId_glob!=-1:
        user_obj = User.objects.get(id=userId_glob)
        user_in_obj = User_Input.objects.get(Q(status='ongoing') ,user_id=user_obj)
        try:
            hotel=Hotel_Booking.objects.get(trip_id = user_in_obj, payment="Remain")
        except:
            hotel=None

        if hotel!=None:
            wallet_obj=User_Account.objects.get(user_id=user_obj)
            if wallet_obj.account_balance>=hotel.charge_hotel:
                wallet_obj.account_balance=wallet_obj.account_balance-hotel.charge_hotel
                wallet_obj.save()
                hotel.payment='Done'
                hotel.save()
                user_in_obj.status='Booked'
                user_in_obj.save()

                return HttpResponseRedirect('/home')
            else:
                error="*You havn't enuff balance in your wallet!!! Do some Credit"
                context={
                    'obj': hotel,
                    'wallet_error':error
                }
            return render(request,'alreadyBooked.html', context)   
        else:
            return HttpResponseRedirect('/bookHotel')
    else:
        return HttpResponseRedirect('/userLogin')

def cancelBooking(request, pk):
    if userId_glob!=-1:
        user_obj = User.objects.get(id=userId_glob)
        hotel=Hotel_Booking.objects.get(id=pk)
        user_in_obj = User_Input.objects.get(trip_id=hotel.trip_id.trip_id)
        if hotel!=None:
            wallet_obj=User_Account.objects.get(user_id=user_obj)
            wallet_obj.account_balance=wallet_obj.account_balance+hotel.charge_hotel
            wallet_obj.save()
            
            hotel.delete()    
            user_in_obj.status=('ongoing')
            user_in_obj.save()

        return HttpResponseRedirect('/bookHotelOrNo')
    else:
        return HttpResponseRedirect('/userLogin')


def bookHotelOrNo(request):
    if userId_glob!=-1:
        user_obj = User.objects.get(id=userId_glob)
        user_in_obj = User_Input.objects.get(Q(status='ongoing') ,user_id=user_obj)

        obj = Hotel_Booking.objects.filter(trip_id = user_in_obj).all()
        if(len(obj)>0):
            return HttpResponseRedirect('/alreadyBooked')


        hotel_obj = Hotel.objects.filter(dest_id = user_in_obj.dest_id).all()
        
        for obj in hotel_obj:
            book_obj = Hotel_Booking.objects.filter(hotel_id = obj, payment='done', date_of_booking_hotel = user_in_obj.starting_date, ending_date=user_in_obj.ending_date).all()
            c=0
            tp=0
        
            for room in book_obj:
                c+=room.no_of_room

            if c>=obj.hotel_capacity:
                obj.delete()
                #dict_hotel.append(obj)

        context={
            'hotel_list':hotel_obj,
            'enable': "yes"
        }
        return render(request, 'bookHotel.html', context)
    else:
        return HttpResponseRedirect('/userLogin')
        

