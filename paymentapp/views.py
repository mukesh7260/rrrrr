from django.shortcuts import render
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            amount = request.data.get('amount')
            description = request.data.get('description')

            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                description=description,
            )

            payment = Payment.objects.create(
                stripe_payment_intent_id=payment_intent['id'],
                amount=amount,
                currency='usd',
                description=description,
                status=payment_intent['status'],
            )

            return Response({
                'client_secret': payment_intent['client_secret'],
                'stripe_payment_intent_id': payment_intent['id']
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class WebhookView(APIView):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
            )
        except ValueError as e:
            return Response({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

        # Handle the event
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent['id'])
            payment.status = 'succeeded'
            payment.save()

        return Response(status=status.HTTP_200_OK)


def payment_page(request):
    context = {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'payment.html', context)



from django.views.generic.base import TemplateView
class HomePageView(TemplateView):
    template_name = "home.html"
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context 
    
def charge(request):
    if request.method == "POST":
        charge = stripe.Charge.create(
            amount = 500,
            currency='INR',
            description='payement Gateway',
            source=request.POST['stripeToken']
        )
        return render(request, 'charge.html')