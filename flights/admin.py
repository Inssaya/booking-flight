from django.contrib import admin
from .models import Airport, Flight, Seat, Booking, User

admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Seat)
admin.site.register(Booking)
# Si tu as custom User :
