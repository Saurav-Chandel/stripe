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
    template_name = "landing_page.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Book")
        context = super(LandingPage, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class SuccessView(TemplateView):
    template_name = "success.html"



class CancelView(TemplateView):
    template_name = "cancel.html"



class CreateCheckoutSessionView(View):
    def post(self,request,*args,**kwargs):
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': '{{PRICE_ID}}',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success.html',
                cancel_url=YOUR_DOMAIN + '/cancel.html',
            )
        except Exception as e:
            return str(e)
    
        return redirect(checkout_session.url, code=303)
    