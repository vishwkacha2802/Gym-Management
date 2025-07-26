from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home/home.html')

def homegeneral(request):
    return render(request, 'home/homegeneral.html')

def homereg(request):
    return render(request, 'home/homereg.html')