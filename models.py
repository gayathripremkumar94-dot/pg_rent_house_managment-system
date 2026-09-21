from django.db import models
from accounts.models import CustomUser
from properties.models import Property


class Booking(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    booking_date = models.DateTimeField(auto_now_add=True)
    move_in_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    total_amount = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"
class Payment(models.Model):

    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    )

    PAYMENT_METHODS = (
        ('UPI', 'UPI'),
        ('Card', 'Card'),
        ('Cash', 'Cash'),
    )

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)

    amount = models.IntegerField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='Pending'
    )

    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment - {self.booking.id}"

# Create your models here.
