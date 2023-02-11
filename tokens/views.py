from django.shortcuts import render
from .models import Token

# Create your views here.
def index(request):
    
    return render(request, "tokens.html")