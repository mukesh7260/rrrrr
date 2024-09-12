
from django.contrib import admin
from paymentapp.models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['stripe_payment_intent_id', 'amount', 'currency','description', 'status', 'created_at','status']

