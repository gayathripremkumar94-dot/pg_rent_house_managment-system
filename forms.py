from django import forms
from .models import Booking, Payment


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ('move_in_date', 'total_amount')


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ('amount', 'payment_method', 'transaction_id')