
from django.urls import path
from . import views

app_name = 'flights'

urlpatterns = [
    # espace utilisateur
    path('', views.home, name='home'),
    path('flight/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('book/<int:flight_id>/', views.book_ticket, name='book_ticket'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),

    # espace admin « front »
    path('admin/dashboard/',            views.admin_dashboard, name='admin_dashboard'),

    # Airports
    path('admin/airport/add/',          views.airport_add,      name='airport_add'),
    path('admin/airport/<int:pk>/edit/',   views.airport_edit,   name='airport_edit'),
    path('admin/airport/<int:pk>/delete/', views.airport_delete, name='airport_delete'),

    # Flights
    path('admin/flight/add/',           views.flight_add,      name='flight_add'),
    path('admin/flight/<int:pk>/edit/',    views.flight_edit,    name='flight_edit'),
    path('admin/flight/<int:pk>/delete/',  views.flight_delete,  name='flight_delete'),

    # Seats
    path('admin/seat/add/',             views.seat_add,        name='seat_add'),
    path('admin/seat/<int:pk>/edit/',      views.seat_edit,      name='seat_edit'),
    path('admin/seat/<int:pk>/delete/',    views.seat_delete,    name='seat_delete'),
]
