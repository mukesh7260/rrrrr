
from django.contrib import admin
from django.urls import path
from paymentapp import views 
from paymentapp.views import payment_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-payment-intent/', views.CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('webhook/', views.WebhookView.as_view(), name='webhook'),
    path('payment/', payment_page, name='payment_page'),
    path('',views.HomePageView.as_view()),
    path('charge/',views.charge, name='charge'),
]
