from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test, login_required
from backend.models import Clients, Hotels, Trip, Flight
from django.contrib.auth.models import User, Group
from django.views.generic.edit import UpdateView
from django.db.models import Q
from django.utils import timezone


# Create your views here.

def index(request):
    return render(request, "frontend/home.html")

def profile(request):  
    if not request.user.is_authenticated:
        return redirect ('frontend')

    return render(request, "frontend/profile.html")
