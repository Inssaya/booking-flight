from django import forms
from .models import Booking, Airport, Flight, Seat
class BookingForm(forms.ModelForm):
    class Meta:
        model  = Booking
        fields = ['flight', 'seat']


class AirportForm(forms.ModelForm):
    class Meta:
        model  = Airport
        fields = ['name', 'city', 'country']


class FlightForm(forms.ModelForm):
    class Meta:
        model  = Flight
        fields = [
            'departure_airport',
            'arrival_airport',
            'departure_time',
            'arrival_time',
            'duration',
            'total_seats',
            'price',
        ]


class SeatForm(forms.ModelForm):
    class Meta:
        model  = Seat
        fields = ['flight', 'seat_number', 'reserved']


class SearchForm(forms.Form):
    departure_airport = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        label="Aéroport de départ",
        required=False
    )
    arrival_airport = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        label="Aéroport d’arrivée",
        required=False
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date de départ",
        required=False
    )
    min_price = forms.DecimalField(label="Prix min", required=False, min_value=0)
    max_price = forms.DecimalField(label="Prix max", required=False, min_value=0)
