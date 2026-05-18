from django.shortcuts import render
from Users.models import UserRegistrationModel 

def base(request):
    return render (request,'base.html')

def home(request):
    return render (request,'home.html')

def userlogin(request):
    return render (request,'userlogin.html')

