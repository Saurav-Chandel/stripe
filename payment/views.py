from django.shortcuts import render,redirect
from rest_framework.views import View
from django.views.generic import TemplateView
import stripe
from django.conf import settings
from payment.models import *
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.http import JsonResponse, HttpResponse
# Create your views here.

class LandingPage(TemplateView):
    template_name = "checkout.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Book")
        context = super(LandingPage, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        print(context)
        return context


class SuccessView(TemplateView):
    template_name = "success.html"



class CancelView(TemplateView):
    template_name = "cancel.html"



class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


        
    