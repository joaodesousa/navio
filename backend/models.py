from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Clients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, verbose_name="Morada")
    nif = models.CharField(max_length=9, verbose_name="NIF", validators=[RegexValidator(r'^\d{1,10}$')], unique=True, null=True)
    mobile = models.CharField(max_length=9, verbose_name="Telemóvel", validators=[RegexValidator(r'^\d{1,10}$')])

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name_plural = "Clientes"
    
    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Clients.objects.create(user=instance)
            instance.clients.save()

    

class Hotels(models.Model):
    hotel_name = models.CharField(max_length=30, verbose_name="Nome", primary_key=True)
    address = models.CharField(max_length=30, verbose_name="Morada")
    city = models.CharField(max_length=10, verbose_name="Cidade")
    mobile = models.CharField(max_length=9, verbose_name="Telemóvel", validators=[RegexValidator(r'^\d{1,10}$')])

    def __str__(self):
        return "%s" % (self.hotel_name)

    class Meta:
        verbose_name_plural = "Hotéis"

class AirCompany(models.Model):
    company_name = models.CharField(max_length=10, verbose_name="Nome", primary_key=True)


    def __str__(self):
        return "%s" % (self.company_name)

    class Meta:
        verbose_name_plural = "Companhias"

class Airport(models.Model):
    airport_name = models.CharField(max_length=200, verbose_name="Aeroporto")
    airport_city = models.CharField(max_length=200, verbose_name="Cidade")
    airport_country = models.CharField(max_length=200, verbose_name="País")

    def __str__(self):
        return "%s" % (self.airport_name)

    class Meta:
        verbose_name_plural = "Aeroportos"

class Flight(models.Model):
    date = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Data")
    flight_id = models.CharField(max_length=10, verbose_name="Ref. Voo")
    company = models.ForeignKey(AirCompany, null=True, on_delete=models.SET_NULL, verbose_name="Companhia")
    airport = models.ForeignKey(Airport, null=True, on_delete=models.SET_NULL, verbose_name="Aeroporto")

    def __str__(self):
        return "%s" % (self.flight_id)

    class Meta:
        verbose_name_plural = "Voos"

class Trip(models.Model):
    trip_id = models.CharField(max_length=20, verbose_name="Ref. Viagem", primary_key=True)
    destination = models.CharField(max_length=200, null=True, verbose_name='Destino')
    client = models.ForeignKey(Clients, null=True, on_delete=models.CASCADE, verbose_name="Cliente")
    out_flight = models.ForeignKey(Flight, related_name="outbound_flight" ,null=True, on_delete=models.SET_NULL, verbose_name="Voo Ida")
    hotel = models.ForeignKey(Hotels, null=True, on_delete=models.SET_NULL, verbose_name="Hotel")
    in_flight = models.ForeignKey (Flight, related_name="inbound_flight", null=True, on_delete=models.SET_NULL, verbose_name="Voo Regresso")
    
    def __str__(self):
        return "%s" % (self.trip_id)

    class Meta:
        verbose_name_plural = "Viagens"