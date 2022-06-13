from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', LandingPage.as_view(), name='landing_page'),
    path('webhooks/stripe/', Stripe_webhook, name='stripe-webhook'),
    path('create-payment-intent/<pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session')
]
