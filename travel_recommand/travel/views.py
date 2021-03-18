from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):
    return render(request, 'index.html')

def userRegister(request):
    return render(request, 'userRegister.html')
