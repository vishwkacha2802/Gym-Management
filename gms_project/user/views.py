from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from .models import Useruser
# from django.db.utils import IntegrityError

def userdashboard(request):
    return render(request, 'user/userdashboard.html')

def userlogin(request):
    return render(request, 'user/userlogin.html')

def userregister(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('userregister')

        if Useruser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('/user/userregister')

        if Useruser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('/user/userregister')

        hashed_password = make_password(password)

        Useruser.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=hashed_password
        )
        messages.success(request, 'Trainer registered successfully')
        return redirect('userlogin')

    return render(request, 'user/userregister.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = Useruser.objects.get(username=username)

            # compare raw password with stored hashed password
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                messages.success(request, 'Login Successful!')
                return redirect('/user/userdashboard/')
            else:
                messages.error(request, 'Invalid password')
                return redirect('/user/userlogin')
        except Useruser.DoesNotExist:
            messages.error(request, 'Username does not exist')
            return redirect('/user/userlogin')
    else:
        return render(request, 'user/userlogin.html')


def logout(request):
    request.session.flush()  # Clears the session
    messages.success(request, "Logged out successfully")
    return redirect('/user/userlogin/')



def userdashboard(request):
    user_id = request.session.get('user_id')

    if user_id is None:
        return redirect('/user/userlogin/')  # Not logged in

    try:
        user = Useruser.objects.get(id=user_id)
    except Useruser.DoesNotExist:
        return redirect('/user/userlogin/')

    return render(request, 'user/userdashboard.html', {
        'user': user
    })
