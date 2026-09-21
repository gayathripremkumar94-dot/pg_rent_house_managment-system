from django.contrib import admin
from .models import Booking, Payment


class PaymentInline(admin.StackedInline):
    model = Payment
    can_delete = False


class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'status', 'booking_date', 'move_in_date', 'total_amount')
    list_filter = ('status',)
    search_fields = ('user__username', 'property__title')
    inlines = [PaymentInline]


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'payment_method', 'status', 'payment_date')
    list_filter = ('status', 'payment_method')


admin.site.register(Booking, BookingAdmin)
admin.site.register(Payment, PaymentAdmin)