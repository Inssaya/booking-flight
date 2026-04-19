from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.db import transaction

from .models import Flight, Booking, Seat, Airport
from .form import (
    SearchForm, BookingForm,
    AirportForm, FlightForm, SeatForm
)

def generate_seats_for_flight(flight):
    totale_seats = flight.total_seats
    seats_created = []
    seat_letters = ['A', 'B', 'C', 'D', 'E', 'F']
    seat_per_row = len(seat_letters)

    import math
    row_needed = math.ceil(totale_seats / seat_per_row)

    seat_number = 1
    for row in range(1, row_needed + 1):
        for letter in seat_letters:
            if seat_number <= totale_seats:
                seat_code = f"{row}{letter}"
                seat, created = Seat.objects.get_or_create(
                    flight=flight,
                    seat_number=seat_code,
                    defaults={'reserved': False}
                )
                if created:
                    seats_created.append(seat)
                seat_number += 1
            else:
                break

    return seats_created


@login_required
def home(request):
    form = SearchForm(request.GET or None)
    qs = Flight.objects.all()

    if form.is_valid():
        dep, arr = form.cleaned_data['departure_airport'], form.cleaned_data['arrival_airport']
        date = form.cleaned_data['date']
        min_p, max_p = form.cleaned_data['min_price'], form.cleaned_data['max_price']

        if dep:
            qs = qs.filter(departure_airport=dep)
        if arr:
            qs = qs.filter(arrival_airport=arr)
        if date:
            qs = qs.filter(departure_time__date=date)
        if min_p is not None:
            qs = qs.filter(price__gte=min_p)
        if max_p is not None:
            qs = qs.filter(price__lte=max_p)

    paginator = Paginator(qs.order_by('departure_time'), 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'flights/home.html', {
        'form': form,
        'page_obj': page_obj,
    })

@login_required
def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    
    # Check if seats exist, if not create them
    if not Seat.objects.filter(flight=flight).exists():
        generate_seats_for_flight(flight)
    
    # Get all seats with their status
    all_seats = Seat.objects.filter(flight=flight).order_by('seat_number')
    available_seats = all_seats.filter(reserved=False)
    
    # Group seats by row for display
    seats_by_row = {}
    for seat in all_seats:
        # Extract row number from seat_number (e.g., "12A" -> 12)
        row_num = ''.join(filter(str.isdigit, seat.seat_number))
        if row_num not in seats_by_row:
            seats_by_row[row_num] = []
        seats_by_row[row_num].append(seat)
    
    # Sort rows numerically
    sorted_rows = sorted(seats_by_row.items(), key=lambda x: int(x[0]))
    
    return render(request, 'flights/flight_detail.html', {
        'flight': flight,
        'seats': available_seats,
        'seats_by_row': sorted_rows,
        'total_seats': all_seats.count(),
        'available_count': available_seats.count(),
        'occupied_count': all_seats.filter(reserved=True).count(),
    })

@login_required
def book_ticket(request, flight_id):
    if request.method != 'POST':
        return redirect('flights:flight_detail', flight_id=flight_id)
    
    flight = get_object_or_404(Flight, id=flight_id)
    seat_id = request.POST.get('seat_id')
    
    if not seat_id:
        messages.error(request, "Please select a seat.")
        return redirect('flights:flight_detail', flight_id=flight_id)
    
    with transaction.atomic():
        try:
            seat = get_object_or_404(
                Seat,
                id=seat_id,
                flight=flight,
                reserved=False
            )
        except Http404:
            messages.error(request, "The selected seat is no longer available.")
            return redirect('flights:flight_detail', flight_id=flight_id)

        # Check if user already has a booking for this flight
        existing_booking = Booking.objects.filter(
            user=request.user,
            flight=flight
        ).first()
        
        if existing_booking:
            messages.error(request, "You already have a booking for this flight.")
            return redirect('flights:my_bookings')

        # Create the booking
        booking = Booking.objects.create(
            user=request.user,
            flight=flight,
            seat=seat,
            status=1  # Confirmed
        )
        
        # Mark seat as reserved
        seat.reserved = True
        seat.save()

    messages.success(request, f"Your booking has been confirmed! Seat {seat.seat_number}")
    return redirect('flights:my_bookings')

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related(
        'flight__departure_airport',
        'flight__arrival_airport',
        'seat'
    ).order_by('-date_booked')
    
    return render(request, 'flights/my_bookings.html', {
        'bookings': bookings
    })

@staff_member_required
def admin_dashboard(request):
    airports = Airport.objects.all()
    flights = Flight.objects.all().select_related('departure_airport', 'arrival_airport')
    bookings = Booking.objects.select_related('user', 'flight', 'seat')
    
    # Calculate statistics
    stats = {
        'total_airports': airports.count(),
        'total_flights': flights.count(),
        'total_bookings': bookings.count(),
        'confirmed_bookings': bookings.filter(status=1).count(),
    }
    
    return render(request, 'flights/admin/dashboard.html', {
        'airports': airports,
        'flights': flights,
        'bookings': bookings,
        'stats': stats,
    })

@staff_member_required
def airport_add(request):
    form = AirportForm(request.POST or None)
    if form.is_valid():
        airport = form.save()
        messages.success(request, f"Airport '{airport.name}' added successfully!")
        return redirect('flights:admin_dashboard')
    return render(request, 'flights/admin/airport_form.html', {'form': form})

@staff_member_required
def flight_add(request):
    form = FlightForm(request.POST or None)
    if form.is_valid():
        with transaction.atomic():
            flight = form.save()
            # Automatically generate seats for the flight
            seats_created = generate_seats_for_flight(flight)
            messages.success(
                request, 
                f"Flight {flight} added successfully with {len(seats_created)} seats!"
            )
        return redirect('flights:admin_dashboard')
    return render(request, 'flights/admin/flight_form.html', {'form': form})

@staff_member_required
def seat_add(request):
    form = SeatForm(request.POST or None)
    if form.is_valid():
        seat = form.save()
        messages.success(request, f"Seat {seat.seat_number} added successfully!")
        return redirect('flights:admin_dashboard')
    return render(request, 'flights/admin/seat_form.html', {'form': form})

@staff_member_required
def airport_edit(request, pk):
    obj = get_object_or_404(Airport, pk=pk)
    form = AirportForm(request.POST or None, instance=obj)
    if form.is_valid():
        airport = form.save()
        messages.success(request, f"Airport '{airport.name}' updated successfully!")
        return redirect('flights:admin_dashboard')
    return render(request, 'flights/admin/airport_form.html', {'form': form, 'object': obj})

@staff_member_required
def airport_delete(request, pk):
    obj = get_object_or_404(Airport, pk=pk)
    if request.method == 'POST':
        name = obj.name
        obj.delete()
        messages.success(request, f"Airport '{name}' deleted successfully!")
        return redirect('flights:admin_dashboard')
    return render(request, 'flights/admin/airport_confirm_delete.html', {'object': obj})

@staff_member_required
def flight_edit(request, pk):
    obj = get_object_or_404(Flight, pk=pk)
    old_total_seats = obj.total_seats
    
    form = FlightForm(request.POST or None, instance=obj)
    if form.is_valid():
        with transaction.atomic():
            flight = form.save()
            
            # If total_seats changed, regenerate seats
            if flight.total_seats != old_total_seats:
                # Delete existing seats that aren't booked
                Seat.objects.filter(flight=flight, reserved=False).delete()
                # Regenerate all seats
                seats_created = generate_seats_for_flight(flight)
                messages.success(
                    request, 
                    f"Flight updated! Seat configuration updated with {len(seats_created)} new seats."
                )
            else:
                messages.success(request, "Flight updated successfully!")
                
        return redirect('flights:admin_dashboard')
    return render(request, 'flights/admin/flight_form.html', {'form': form, 'object': obj})

@staff_member_required
def flight_delete(request, pk):
    obj = get_object_or_404(Flight, pk=pk)
    if request.method == 'POST':
        flight_info = str(obj)
        obj.delete()
        messages.success(request, f"Flight '{flight_info}' deleted successfully!")
        return redirect('flights:admin_dashboard')
    return render(request, 'flights/admin/flight_confirm_delete.html', {'object': obj})

@staff_member_required
def seat_edit(request, pk):
    obj = get_object_or_404(Seat, pk=pk)
    form = SeatForm(request.POST or None, instance=obj)
    if form.is_valid():
        seat = form.save()
        messages.success(request, f"Seat {seat.seat_number} updated successfully!")
        return redirect('flights:admin_dashboard')
    return render(request, 'flights/admin/seat_form.html', {'form': form, 'object': obj})

@staff_member_required
def seat_delete(request, pk):
    obj = get_object_or_404(Seat, pk=pk)
    if request.method == 'POST':
        seat_info = f"{obj.seat_number} (Flight {obj.flight.id})"
        obj.delete()
        messages.success(request, f"Seat {seat_info} deleted successfully!")
        return redirect('flights:admin_dashboard')
    return render(request, 'flights/admin/seat_confirm_delete.html', {'object': obj})


def generate_seats_for_flight(flight):
    """Generate seats in airplane layout (6 seats per row: ABC DEF)"""
    total_seats = flight.total_seats
    seats_created = []
    
    seat_letters = ['A', 'B', 'C', 'D', 'E', 'F']
    rows_needed = (total_seats + 5) // 6  # Ceiling division
    
    seat_number = 1
    for row in range(1, rows_needed + 1):
        for letter in seat_letters:
            if seat_number > total_seats:
                break
            seat_code = f"{row}{letter}"
            seat, created = Seat.objects.get_or_create(
                flight=flight,
                seat_number=seat_code,
                defaults={'reserved': False}
            )
            if created:
                seats_created.append(seat)
            seat_number += 1
    
    return seats_created