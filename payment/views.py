from django.shortcuts import render,redirect
from rest_framework.views import View
from django.views.generic import TemplateView
import stripe
from django.conf import settings
from payment.models import *
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
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
        print('_______________________')
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        print(product)
        print(product.price)
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
                            'images': ['https://i.imgur.com/EHyR2nP.png'],
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

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def Stripe_webhook(request):
  print("+++++++++++")
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  # Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']
    print(session)

    customer_email=session['customer_details']['email']
    product_id=session['metadata']['product_id']

    product=Product.objects.get(id=product_id)

    send_mail(
        subject="Here is your Product",
        message=f"Thanx for your purchase,Here is the product you ordered {product.url}",
        recipient_list=[customer_email],
        from_email="chandelsaurav0817@gmail.com"
    )

  # Passed signature verification
  return HttpResponse(status=200)
        
import json
class StripeIntentView(View):
    def post(self,request,*args,**kwargs):
        try:
            print('________________')
            req_json = json.loads(request.body)
            print(req_json)
            customer = stripe.Customer.create(email=req_json['email'])
            print(customer)
            product_id = self.kwargs["pk"]
            product = Product.objects.get(id=product_id)
            intent = stripe.PaymentIntent.create(
                amount=product.price,
                currency='inr',
                customer=customer['id'],
                metadata={
                    "product_id": product.id
                }
            )
            print(intent)
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({ 'error': str(e) })              