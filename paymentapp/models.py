# payments/models.py

from django.db import models

class Payment(models.Model):
    stripe_payment_intent_id = models.CharField(max_length=255)
    amount = models.IntegerField()
    currency = models.CharField(max_length=10, default='usd')
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    
    def __str__(self):
        return f'Payment {self.stripe_payment_intent_id}'

