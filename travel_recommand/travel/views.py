from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):
    return render(request, 'index.html')

def userRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        email = request.POST.get('mail')
        contact = request.POST.get('contact')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        
        if cpassword == password:
            if(gender=='Male'):
                gender='M'
            elif(gender=='Female'):
                gender='F'
            else:
                gender='O'

            user = User(username=username, password=password,                        # Create object of table to store the data
                        email=email, contact=contact, gender=gender, dob=dob)
            try:  
                user.save()
                return render(request, 'userInput.html')
            except Exception as e:
                print(e)
                errors = "*We found the same username or email id in our data. These should be unique. Try some new"
                context = {
                    'username': username,
                    'mail': email,
                    'contact': contact,
                    'gender': gender,
                    'errors': errors,
                    'dob': dob,
                }
                return render(request, 'userRegister.html', context)
        else:
            errors = "*Both the passwords are not matching. Try again"
            context = {
                    'username': username,
                    'mail': email,
                    'contact': contact,
                    'gender': gender,
                    'errors': errors,
                    'dob': dob,
            }
            return render(request, 'userRegister.html', context)

    return render(request, 'userRegister.html')
    
def userLogin(request):
    if request.method == "POST":                                            # If Got response from Login Form
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
            return render(request, "userLogin.html", {"errors": error})
        elif not user_obj.password == password:
            errors = "*Invalid password"
            return render(request, "userLogin.html", {"errors": errors, "username": username})
        else:
            return render(request, 'userInput.html')

    return render(request, 'userLogin.html')

def userInput(request):
    return render(request, 'userInput.html')

