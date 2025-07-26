from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Trainer
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, auth
from django.db.utils import IntegrityError


# Create your views here.

def login_check(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            trainer = Trainer.objects.get(username=username)

            # compare raw password with stored hashed password
            if check_password(password, trainer.password):
                request.session['trainer_id'] = trainer.id
                messages.success(request, 'Login Successful!')
                return redirect('/trainer/dashboard')
            else:
                messages.error(request, 'Invalid password')
                return redirect('/trainer/login')
        except Trainer.DoesNotExist:
            messages.error(request, 'Username does not exist')
            return redirect('/trainer/login')
    else:
        return render(request, 'trainer/login.html')


# def login_check(request):
#     username = request.POST["username"]
#     password = request.POST["password"]

#     result = auth.authenticate(username=username, password=password)

#     if result is None:
#         messages.error(request, "Invalid Username or Password")
#         return redirect('/trainer/login')
#     else:
#         auth.login(request, result)
#         return redirect('/trainer/dashboard')

def dashboard(request):
    return render(request, 'trainer/dashboard.html')
    # trainer_id = request.session.get('trainer_id')
    # if not trainer_id:
    #     return redirect('/trainer/login/')  # Require login

    # trainer = Trainer.objects.get(id=trainer_id)
    # return render(request, 'trainer/dashboard.html', {'trainer': trainer})

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if Trainer.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('/trainer/register')

        if Trainer.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('/trainer/register')

        hashed_password = make_password(password)

        Trainer.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=hashed_password
        )
        messages.success(request, 'Trainer registered successfully')
        return redirect('login')

    return render(request, 'trainer/register.html')


def login(request):
    return render(request, 'trainer/login.html')


def logout_trainer(request):
    request.session.flush()  # Clears the session
    messages.success(request, "Logged out successfully")
    return redirect('/trainer/login')



# def register(request):
#     if request.method == 'POST':
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         username = request.POST['username']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']

#         if password != confirm_password:
#             messages.error(request, "Passwords do not match")
#             return redirect('register')

#         if Trainer.objects.filter(username=username).exists():
#             messages.error(request, 'Username already taken')
#             return redirect('register')

#         if Trainer.objects.filter(email=email).exists():
#             messages.error(request, 'Email already registered')
#             return redirect('register')

#         hashed_password = make_password(password)

#         Trainer.objects.create(
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             username=username,
#             password=hashed_password
#         )
#         messages.success(request, 'Trainer registered successfully')
#         return redirect('login')

#     return render(request, 'trainer/register.html')

def dashboard(request):
    trainer_id = request.session.get('trainer_id')

    if trainer_id is None:
        return redirect('/trainer/login')  # Not logged in

    try:
        trainer = Trainer.objects.get(id=trainer_id)
    except Trainer.DoesNotExist:
        return redirect('/trainer/login')

    return render(request, 'trainer/dashboard.html', {
        'trainer': trainer
    })

