from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from datetime import datetime
from django.db.models import Q

# Create your views here.
userId_glob=-1
def login(id):
    global  userId_glob
    userId_glob=id

def index(request):
    return render(request, 'index.html')

def userRegister(request): #register page
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
                return render(request, 'userInput.html') #after successfully submitted User can give response in User Input page
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

    return render(request, 'userRegister.html') #otherwise User Register HTML displays
    
def userLogin(request):
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
            return HttpResponseRedirect('/userInput') #after successfully submitted User can give response in User Input page

    return render(request, 'userLogin.html') #otherwise diplays Log IN HTML page

src_name_glob=""
desti_name_glob=""
def userInput(request):

    try:
        dest_available_obj = Destination.objects.all().order_by('dest_name')
    except:
        dest_available_obj = None

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

        return render(request, "userInput.html", {"dest_available_obj": dest_available_obj})

    return render(request, 'userInput.html') #after successfully submitted User can give response in User Input page

def split_userInput(request):
    
    today = datetime.today().strftime('%Y-%m-%d')
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


def placeFetch(request):
    if userId_glob!=-1:
        try:
            user_obj = User.objects.get(id=userId_glob)
            user_in_obj = User_Input.objects.get(Q(status='ongoing') ,user_id=user_obj)
        except:
            user_in_obj=None
        if user_in_obj!=None:
            choice = user_in_obj.visit_place_type
            choice=choice.split(',')
            print(choice)
            place_obj = Place.objects.filter(type_of_Place__in = choice).all().order_by('-extra_charge','rate_place')
            print(len(place_obj))
            
            context={
                'place_obj': place_obj
            }

        return render(request,'placeFetch.html', context)
    else:
        return HttpResponseRedirect('/userLogin')
            