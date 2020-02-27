from django.contrib import admin
from .models import Clients, Hotels, AirCompany, Airport, Flight, Trip

# Register your models here.


admin.site.register(Trip)
admin.site.register(Clients)
admin.site.register(Hotels)
admin.site.register(AirCompany)
admin.site.register(Airport)
admin.site.register(Flight)