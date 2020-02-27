from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.backend, name="backend"),
    path("clientes/", views.clients, name="clients"),
    path("clientes/<int:nif>", views.client_det, name="client_det"),
    path("clientes/<int:nif>/update/", views.client_upd, name='client_upd'),
    path("clientes/novo/", views.signup, name="newclient"),
    path("viagens/", views.trips, name="trips"),
    path("viagens/detail/<trip_id>/", views.trip_det, name="trip_det"),
    path("viagens/novo/", views.newtrip, name="newtrip"),
    path("hotel/", views.hotel, name="hotel"),
    path("hotel/novo/", views.newhotel, name="newhotel"),
    path("flights/", views.flights, name="flights"),
    path("flights/novo/", views.newflight, name="newflight"),
    path("accounts/", include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)