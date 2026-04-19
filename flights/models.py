from django.db import models
from django.contrib.auth.models import User

class Airport(models.Model):
    name    = models.CharField(max_length=100)
    city    = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.city}, {self.country}"


class Flight(models.Model):
    departure_airport = models.ForeignKey(
        Airport, related_name="departures", on_delete=models.CASCADE
    )
    arrival_airport   = models.ForeignKey(
        Airport, related_name="arrivals",   on_delete=models.CASCADE
    )
    departure_time = models.DateTimeField()
    arrival_time   = models.DateTimeField()
    duration       = models.DurationField()
    total_seats    = models.IntegerField()
    price          = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Vol {self.id} : {self.departure_airport} → {self.arrival_airport}"


class Seat(models.Model):
    flight      = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    reserved    = models.BooleanField(default=False)

    def __str__(self):
        return f"Siège {self.seat_number} - {self.flight}"


class Booking(models.Model):
    STATUS_CHOICES = [
        (0, "En attente"),
        (1, "Confirmé"),
    ]

    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    flight      = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat        = models.ForeignKey(Seat, on_delete=models.CASCADE)
    date_booked = models.DateTimeField(auto_now_add=True)
    status      = models.IntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return f"Réservation {self.id} : {self.user.username} / {self.flight} / Siège {self.seat.seat_number}"
