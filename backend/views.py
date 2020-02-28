from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Clients, Hotels, Trip, Flight
from django.contrib.auth.models import User
from .forms import SignUpForm, UpdateClient, NewTrip, NewHotel, NewFlight, NewCompany, NewAirport
from django.views.generic.edit import UpdateView
from django.db.models import Q
from django.utils import timezone


# Dashboard

@login_required(login_url='./accounts/login/')
def backend(request):
    ClientCount= Clients.objects.all().count()
    ClientsTrip= Clients.objects.all()
    TripCount = Trip.objects.all().count()
    HotelCount = Hotels.objects.all().count()
    FlightCount = Flight.objects.all().count()
    Going = Flight.objects.filter(date__gt=timezone.now()).order_by('date')
    ClientsArriving = Clients.objects.filter(trip__in_flight__date__gt=timezone.now())
    ClientsLeaving = Clients.objects.filter(trip__out_flight__date__gt=timezone.now()) 
    ClientsDash = ClientsArriving | ClientsArriving
    context = {'ClientCount': ClientCount, 'ClientsTrip': ClientsTrip, 'TripCount': TripCount, 'HotelCount': HotelCount, 'FlightCount': FlightCount, 'Going': Going, 'ClientsDash': ClientsDash}
    return render(request, "backend/home.html", context)

# Clients

@login_required(login_url='./accounts/login/')
def clients(request):
    u = User.objects.filter(is_superuser=False)
    context= {'u': u}
    return render(request, "backend/clients.html", context)

@login_required(login_url='../accounts/login/')
def client_upd(request, nif):
    ls= Clients.objects.get(nif=nif)
    if request.method == 'POST':
        form = UpdateClient(request.POST, instance=ls.user)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.clients.address = form.cleaned_data.get('address')
            user.clients.nif = form.cleaned_data.get('nif')
            user.clients.mobile = form.cleaned_data.get('mobile')
            user.clients.save()
            return redirect('clients')
    else:
        form = UpdateClient(instance=ls.user, initial={'nif': ls.user.clients.nif, 'mobile': ls.user.clients.mobile, 'address': ls.user.clients.address })
    return render(request, 'backend/client_update.html', {'form': form, 'ls': ls})

@login_required(login_url='../accounts/login/')
def client_det(request, nif):
   ls= Clients.objects.get(nif=nif)
   ts= Trip.objects.filter(client = ls)
   context = {'ls': ls, 'ts' : ts}
   return render(request, "backend/client_detail.html", context)

@login_required(login_url='./accounts/login/')
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # this creates the user with first_name, email and last_name as well!
            user.refresh_from_db()  # load the profile instance created by the signal
            user.clients.address = form.cleaned_data.get('address')
            user.clients.nif = form.cleaned_data.get('nif')
            user.clients.mobile = form.cleaned_data.get('mobile')
            user.clients.save()
            return redirect('clients')
    else:
        form = SignUpForm()
    return render(request, 'backend/new_client.html', {'form': form})


# Trips

@login_required(login_url='./accounts/login/')
def trips(request):
    trs= Trip.objects.all()
    context= {'trs' : trs}
    return render(request, "backend/trips.html", context)

@login_required(login_url='./accounts/login/')
def trip_det(request, trip_id):
    tdrs= Trip.objects.get(trip_id=trip_id)
    tdc = Clients.objects.filter(trip=tdrs)
    vs = Flight.objects.filter(inbound_flight=tdrs) 
    ve = Flight.objects.filter(outbound_flight=tdrs) 
    context= {'tdrs' : tdrs, 'tdc': tdc, 'vs': vs, 've': ve}
    return render(request, "backend/trips_det.html", context)

@login_required(login_url='./accounts/login/')
def newtrip(request):
    if request.method == 'POST':
        form = NewTrip(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trips')
    else:
        form = NewTrip()
    return render(request, 'backend/new_trip.html', {'form': form})

# Hotel

@login_required(login_url='./accounts/login/')
def hotel (request):
    hs= Hotels.objects.all()
    context= {'hs' : hs}
    return render(request, "backend/hotel.html", context)

@login_required(login_url='./accounts/login/')
def newhotel(request):
    if request.method == 'POST':
        form = NewHotel(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hotel')
    else:
        form = NewHotel()
    return render(request, 'backend/new_hotel.html', {'form': form})

# Flight

@login_required(login_url='./accounts/login/')
def flights (request):
    fs= Flight.objects.all()
    context= {'fs' : fs}
    return render(request, "backend/flight.html", context)

@login_required(login_url='./accounts/login/')
def newflight(request):
    if request.method == 'POST':
        form = NewFlight(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flights')
    else:
        form = NewFlight()
    return render(request, 'backend/new_flight.html', {'form': form})

# AirCompany

@login_required(login_url='./accounts/login/')
def newcompany(request):
    if request.method == 'POST':
        form = NewCompany(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flights')
    else:
        form = NewCompany()
    return render(request, 'backend/new_company.html', {'form': form})

# Airport

@login_required(login_url='./accounts/login/')
def newairport(request):
    if request.method == 'POST':
        form = NewAirport(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flights')
    else:
        form = NewAirport()
    return render(request, 'backend/new_airport.html', {'form': form})