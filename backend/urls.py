from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.backend, name="backend"),
    path("clientes/", views.clients, name="clients"),
    path("clientes/<int:nif>", views.client_det, name="client_det"),
    path("clientes/<int:nif>/update/", views.client_upd, name='client_upd'),
    path("clientes/<int:id>/delete/", views.client_del, name='client_del'),
    path("clientes/novo/", views.signup, name="newclient"),
    path("viagens/", views.trips, name="trips"),
    path("viagens/detail/<trip_id>/", views.trip_det, name="trip_det"),
    path("viagens/detail/<trip_id>/update/", views.trip_upd, name='trip_upd'),
    path("viagens/detail/<trip_id>/delete/", views.trip_del, name='trip_del'),
    path("viagens/novo/", views.newtrip, name="newtrip"),
    path("hotel/", views.hotel, name="hotel"),
    path("hotel/novo/", views.newhotel, name="newhotel"),
    path("hotel/<int:id>/update/", views.hotel_upd, name="hotel_upd"),
    path("hotel/<int:id>/delete/", views.hotel_del, name="hotel_del"),
    path("flights/", views.flights, name="flights"),
    path("flights/novo/", views.newflight, name="newflight"),
    path("flights/<int:id>/update", views.flight_upd, name="flight_upd"),
    path("flights/<int:id>/delete", views.flight_del, name="flight_del"),
    path("accounts/", include('django.contrib.auth.urls')),
    path("companhia/novo/", views.newcompany, name="newcompany"),
    path("aeroporto/novo/", views.newairport, name="newairport"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)