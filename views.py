from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking, Payment
from properties.models import Property



@login_required
def create_booking(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        move_in_date = request.POST.get('move_in_date')

        booking = Booking.objects.create(
            user=request.user,
            property=property_obj,
            move_in_date=move_in_date,
            total_amount=property_obj.price
        )

        # Optional: mark property unavailable
        property_obj.is_available = False
        property_obj.save()

        return redirect('payment_page', booking_id=booking.id)

    return render(request, 'booking.html', {'property': property_obj})



@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'my_bookings.html', {'bookings': bookings})



@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking_detail.html', {'booking': booking})



@login_required
def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        transaction_id = request.POST.get('transaction_id')

        Payment.objects.create(
            booking=booking,
            amount=booking.total_amount,
            payment_method=payment_method,
            transaction_id=transaction_id,
            status='Completed'  
        )

        booking.status = 'Confirmed'
        booking.save()

        return redirect('booking_detail', booking_id=booking.id)

    return render(request, 'payment.html', {'booking': booking})



@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status == 'Pending':
        booking.status = 'Cancelled'
        booking.save()

        # Optional: make property available again
        booking.property.is_available = True
        booking.property.save()

    return redirect('my_bookings')



@login_required
def owner_bookings(request):
    bookings = Booking.objects.filter(property__owner=request.user).order_by('-booking_date')
    return render(request, 'owner_bookings.html', {'bookings': bookings})

# Create your views here.
