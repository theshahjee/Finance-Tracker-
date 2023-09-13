from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User, auth 
from datetime import date

# Create your views here.

# Dashboard
def dashboard(request):
    return HttpResponse("<h1>Welcome to Dashboard</h1>")
    # return render(request,"dashboard.html",{})

# Income
def income(request):
    
    return render(request,"income.html",{})

# Index page
def index(request):
    return render(request, "index.html",{})


# Signup 
def signup(request):
    if request.method == "POST":
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        email= request.POST['email']
        password= request.POST['password']

        if User.objects.filter(username=email).exists():
            print("Username is already used")
            return redirect('/')
        else:
            user = User.objects.create_user(username=email,password= password, email=email, first_name=first_name,last_name=last_name)
            user.save()
            print("User Account created successfully")
            return redirect('/')
    return render(request,"index.html",{})
        
# Login
def login(request):
    if request.method== "POST":
        username = request.POST['email']
        password = request.POST['password']

        user= auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            print(f"User {username} is logged in")
            return redirect("/dashboard")
        else:
            print("Invalid Login details")
            return redirect("/")
    else:
        return render(request, "/",{})


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect("/")