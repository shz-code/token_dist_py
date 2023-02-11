from django.shortcuts import render
from .models import Token
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "tokens.html")

def scanner(request):
    return render(request, "scanner.html")

def print(request, num):
    return HttpResponse("Print")