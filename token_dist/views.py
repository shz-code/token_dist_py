from django.shortcuts import render, redirect, HttpResponse
from users.models import User
# Create your views here.

def dashboard(request):
    return render(request, "index.html")