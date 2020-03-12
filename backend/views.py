from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test, login_required
from .models import Clients, Hotels, Trip, Flight
from django.contrib.auth.models import User, Group
from .forms import SignUpForm, UpdateClient, NewTrip, NewHotel, NewFlight, NewCompany, NewAirport, UpdateTrip, UpdateHotel, UpdateFlight, NewEmployee
from django.views.generic.edit import UpdateView
from django.db.models import Q
from django.utils import timezone


# Dashboard

@login_required(login_url='./accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def backend(request):
    ClientCount= Clients.objects.all().count()
    ClientsTrip= Clients.objects.all()
    TripCount = Trip.objects.all().count()
    HotelCount = Hotels.objects.all().count()
    FlightCount = Flight.objects.all().count()
    Going = Flight.objects.filter(date__gt=timezone.now()).order_by('date')
    ClientsDash = Clients.objects.filter(Q(trip__in_flight__date__gt=timezone.now()) | Q(trip__out_flight__date__gt=timezone.now())).distinct()
    context = {'ClientCount': ClientCount, 'ClientsTrip': ClientsTrip, 'TripCount': TripCount, 'HotelCount': HotelCount, 'FlightCount': FlightCount, 'Going': Going, 'ClientsDash': ClientsDash}
    return render(request, "backend/home.html", context)

@login_required(login_url='./accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def newemployee(request):
    if request.method == 'POST':
        form = NewEmployee(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Employees')
            user.groups.add(group)
            return redirect('backend')
    else:
        form = NewEmployee()
    return render(request, 'backend/new_employee.html', {'form': form})

# Clients

@login_required(login_url='./accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def clients(request):
    u = Clients.objects.all()
    context= {'u': u}
    return render(request, "backend/clients.html", context)

@login_required(login_url='../accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def client_upd(request, nif):
    ls= Clients.objects.get(nif=nif)
    if request.method == 'POST':
        form = UpdateClient(request.POST, instance=ls.user)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.clients.address = form.cleaned_data.get('address')
            user.clients.city = form.cleaned_data.get('city')
            user.clients.postal = form.cleaned_data.get('postal')
            user.clients.nif = form.cleaned_data.get('nif')
            user.clients.mobile = form.cleaned_data.get('mobile')
            user.clients.save()
            return redirect('clients')
    else:
        form = UpdateClient(instance=ls.user, initial={'nif': ls.user.clients.nif, 'mobile': ls.user.clients.mobile, 'address': ls.user.clients.address, 'city': ls.user.clients.city, 'postal': ls.user.clients.postal})
    return render(request, 'backend/client_update.html', {'form': form, 'ls': ls})

@login_required(login_url='../accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def client_det(request, nif):
   ls= Clients.objects.get(nif=nif)
   ts= Trip.objects.filter(client = ls)
   TripDash = (Trip.objects.filter(client = ls).filter(Q(in_flight__date__gt=timezone.now()) | Q(out_flight__date__gt=timezone.now())))
   PTripDash = (Trip.objects.filter(client = ls).filter(Q(in_flight__date__lt=timezone.now()) | Q(out_flight__date__lt=timezone.now())))
   context = {'ls': ls, 'ts' : ts, 'TripDash': TripDash, 'PTripDash': PTripDash}
   return render(request, "backend/client_detail.html", context)

@login_required(login_url='./accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients')
    else:
        form = SignUpForm()
    return render(request, 'backend/new_client.html', {'form': form})

@login_required(login_url='../accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def client_del(request, id):
    object = User.objects.get(id=id)
    object.delete()
    return redirect('clients')    


# Trips

@login_required(login_url='./accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def trips(request):
    trs= Trip.objects.all()
    context= {'trs' : trs}
    return render(request, "backend/trips.html", context)

@login_required(login_url='./accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def trip_det(request, trip_id):
    tdrs= Trip.objects.get(trip_id=trip_id)
    tdc = Clients.objects.filter(trip=tdrs)
    vs = Flight.objects.filter(inbound_flight=tdrs) 
    ve = Flight.objects.filter(outbound_flight=tdrs) 
    context= {'tdrs' : tdrs, 'tdc': tdc, 'vs': vs, 've': ve}
    return render(request, "backend/trips_det.html", context)

@login_required(login_url='./accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def newtrip(request):
    if request.method == 'POST':
        form = NewTrip(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trips')
    else:
        form = NewTrip()
    return render(request, 'backend/new_trip.html', {'form': form})

@login_required(login_url='../accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def trip_upd(request, trip_id):
    ts = Trip.objects.get(trip_id=trip_id)
    if request.method == 'POST':
        form = UpdateTrip(request.POST, instance=ts)
        if form.is_valid():
            form.save()
            return redirect('trips')
    else:
        form = UpdateTrip(initial={'trip_id': ts.trip_id, 'destination': ts.destination, 'client': ts.client, 'out_flight': ts.out_flight, 'hotel': ts.hotel, 'in_flight': ts.in_flight})
    return render(request, 'backend/trip_update.html', {'form': form, 'ts': ts})

@login_required(login_url='../accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def trip_del(request, trip_id):
    object = Trip.objects.get(trip_id=trip_id)
    object.delete()
    return redirect('trips')

# Hotel

@login_required(login_url='./accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def hotel (request):
    hs= Hotels.objects.all()
    context= {'hs' : hs}
    return render(request, "backend/hotel.html", context)

@login_required(login_url='./accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def newhotel(request):
    if request.method == 'POST':
        form = NewHotel(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hotel')
    else:
        form = NewHotel()
    return render(request, 'backend/new_hotel.html', {'form': form})

@login_required(login_url='../accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def hotel_upd(request, id):
    hs = Hotels.objects.get(id=id)
    if request.method == 'POST':
        form = UpdateHotel(request.POST, instance=hs)
        if form.is_valid():
            form.save()
            return redirect('hotel')
    else:
        form = UpdateHotel(initial={'hotel_name': hs.hotel_name, 'address': hs.address, 'city': hs.city, 'mobile': hs.mobile})
    return render(request, 'backend/hotel_update.html', {'form': form, 'hs': hs})

@login_required(login_url='../accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def hotel_del(request, id):
    object = Hotels.objects.get(id=id)
    object.delete()
    return redirect('hotel')

# Flight

@login_required(login_url='./accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def flights (request):
    fs= Flight.objects.all()
    context= {'fs' : fs}
    return render(request, "backend/flight.html", context)

@login_required(login_url='./accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def newflight(request):
    if request.method == 'POST':
        form = NewFlight(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flights')
    else:
        form = NewFlight()
    return render(request, 'backend/new_flight.html', {'form': form})

@login_required(login_url='../accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def flight_upd(request, id):
    fs = Flight.objects.get(id=id)
    if request.method == 'POST':
        form = UpdateFlight(request.POST, instance=fs)
        if form.is_valid():
            form.save()
            return redirect('flights')
    else:
        form = UpdateFlight(initial={'date': fs.date, 'flight_id': fs.flight_id, 'company': fs.company, 'airport': fs.airport})
    return render(request, 'backend/flight_update.html', {'form': form, 'fs': fs})

@login_required(login_url='../accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def flight_del(request, id):
    object = Flight.objects.get(id=id)
    object.delete()
    return redirect('flights')

# AirCompany

@login_required(login_url='./accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def newcompany(request):
    if request.method == 'POST':
        form = NewCompany(request.POST)
        if form.is_valid():
            form.save()
            return redirect('newflight')
    else:
        form = NewCompany()
    return render(request, 'backend/new_company.html', {'form': form})

# Airport

@login_required(login_url='./accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Employees').exists())
def newairport(request):
    if request.method == 'POST':
        form = NewAirport(request.POST)
        if form.is_valid():
            form.save()
            return redirect('newflight')
    else:
        form = NewAirport()
    return render(request, 'backend/new_airport.html', {'form': form})