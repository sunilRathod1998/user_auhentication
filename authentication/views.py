from django.contrib import messages
from django.db.models.query_utils import RegisterLookupMixin
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from user_auth import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request, 'home.html')
    
def signup(request):
    if request.method == 'POST':
        usrname = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        conf_pass = request.POST['conf_pass']
        
        # conf_pass = request.POST['conf_pass']
        
        if len(usrname) > 15:
            messages.error(request, "username should be of 15 character")
            return redirect('/signup')

        if User.objects.filter(username=usrname):
            messages.error(request, "use different username")
            return redirect('/signup')

        if User.objects.filter(email=email):
            messages.error(request, "use different email")
            return redirect('/signup')

        if password != conf_pass:
            messages.error(request, "password not matchning")
            return redirect('/signup')

        user = User.objects.create_user(usrname, conf_pass, password)
        user.first_name = fname
        user.last_name = lname
        user.email = email
        user.save()

        # email sender code
        subject = 'wellcome to user_auth'
        message = "hello" + user.first_name + "!! \n" + "wellcome to user_auth \n  thank you for visiting website \n please varify your email"
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request,user)
            fname = user.first_name
            messages.success(request, "loged In successfully")
            return render(request, 'home.html', {'name':fname})

        else:
            messages.error(request, 'bad credential')
            return redirect('/login')
    return render(request, 'login.html')

def signout(request):
    logout(request)
    messages.success(request, "You are Loged Out")
    return redirect('/')