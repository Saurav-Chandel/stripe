from django.shortcuts import render,redirect
from rest_framework.views import View
from django.views.generic import TemplateView
import stripe
from django.conf import settings
from payment.models import *
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.urls import reverse, reverse_lazy
from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

# class LandingPage(TemplateView):
#     template_name = "checkout.html"

#     def get_context_data(self, **kwargs):
#         product = Product1.objects.get(name="raju")
#         context = super(LandingPage, self).get_context_data(**kwargs)
#         context.update({
#             "product": product,
#             "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
#         })
#         print(context)
#         return context


# class SuccessView(TemplateView):
#     template_name = "success.html"


# class CancelView(TemplateView):
#     template_name = "cancel.html"


# class CreateCheckoutSessionView(View):
#     def post(self, request, *args, **kwargs):
#         print('_______________________')
#         product_id = self.kwargs["pk"]
#         product = Product1.objects.get(id=product_id)
#         print(product)
#         print(product.price)
#         YOUR_DOMAIN = "http://127.0.0.1:8000"
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price_data': {
#                         'currency': 'inr',
#                         'unit_amount': product.price,
#                         'product_data': {
#                             'name': product.name,
#                             'images': ['https://i.imgur.com/EHyR2nP.png'],
#                         },
#                     },
#                     'quantity': 1,
#                 },
#             ],
#             metadata={
#                 "product_id": product.id
#             },
#             mode='payment',
#             success_url=YOUR_DOMAIN + '/success/',
#             cancel_url=YOUR_DOMAIN + '/cancel/',
#         )
#         return JsonResponse({
#             'id': checkout_session.id
#         })

# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
# def Stripe_webhook(request):
#   print("+++++++++++")
#   payload = request.body
#   sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#   event = None

#   try:
#     event = stripe.Webhook.construct_event(
#       payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#     )
#   except ValueError as e:
#     # Invalid payload
#     return HttpResponse(status=400)
#   except stripe.error.SignatureVerificationError as e:
#     # Invalid signature
#     return HttpResponse(status=400)

#   # Handle the checkout.session.completed event
#   if event['type'] == 'checkout.session.completed':
#     session = event['data']['object']
#     print(session)

#     customer_email=session['customer_details']['email']
#     product_id=session['metadata']['product_id']

#     product=Product.objects.get(id=product_id)

#     send_mail(
#         subject="Here is your Product",
#         message=f"Thanx for your purchase,Here is the product you ordered {product.url}",
#         recipient_list=[customer_email],
#         from_email="chandelsaurav0817@gmail.com"
#     )

#   # Passed signature verification
#   return HttpResponse(status=200)
        
# import json
# class StripeIntentView(View):
#     def post(self,request,*args,**kwargs):
#         try:
#             print('________________')
#             req_json = json.loads(request.body)
#             print(req_json)
#             customer = stripe.Customer.create(email=req_json['email'])
#             print(customer)
#             product_id = self.kwargs["pk"]
#             product = Product.objects.get(id=product_id)
#             intent = stripe.PaymentIntent.create(
#                 amount=product.price,
#                 currency='inr',
#                 customer=customer['id'],
#                 metadata={
#                     "product_id": product.id
#                 }
#             )
#             print(intent)
#             return JsonResponse({
#                 'clientSecret': intent['client_secret']
#             })
#         except Exception as e:
#             return JsonResponse({ 'error': str(e) })              

####################
class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = 'product_list'
    
    """
    context_object_name - Name of the context object that will hold the list of products. Django will automatically fetch the list of products,
    so that we do not have to write the query to fetch products from the database.
    """

class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    template_name = "product_create.html"
    success_url = reverse_lazy("home")

    
class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    pk_url_kwarg = 'id'

    '''
    Here in this code, we are overriding the get_context_data() method to add publishable key as a data to the template context.
    We set pk_url_kwarg = 'id' to instruct Django to fetch details of the product with the id passed as a URL parameter.
    '''
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        print(context)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLIC_KEY
        print(context)
        return context  

@csrf_exempt
def create_checkout_session(request, id):
    print(id)
    request_data = json.loads(request.body)
    # print(request_data)
    product = get_object_or_404(Product, pk=id)
    # print(product)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        # Customer Email is optional,
        # It is not safe to accept email directly from the client side
        customer_email = request_data['email'],
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                    'name': product.name,
                    },
                    'unit_amount': int(product.price * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('failed')),
    )

    # OrderDetail.objects.create(
    #     customer_email=email,
    #     product=product, ......
    # )

    order = OrderDetail()
    order.customer_email = request_data['email']
    order.product = product
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.amount = int(product.price * 100)
    order.save()

    # return JsonResponse({'data': checkout_session})
    return JsonResponse({'sessionId': checkout_session.id})

class PaymentSuccessView(TemplateView):
    template_name = "payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        # print(session_id)
        if session_id is None:
            return HttpResponseNotFound()
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # print(stripe.api_key)
        session = stripe.checkout.Session.retrieve(session_id)
        # print(session)

        order = get_object_or_404(OrderDetail, stripe_payment_intent=session.payment_intent)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)

class PaymentFailedView(TemplateView):
    template_name = "payment_failed.html"

class OrderHistoryListView(ListView):
    model = OrderDetail
    template_name = "order_history.html"    