from django.db import models

# Create your models here.


class Product1(models.Model):
    name=models.CharField(max_length=200,null=True,blank=True)
    price=models.IntegerField(default=0)
    file = models.FileField(upload_to="product_files/", blank=True, null=True)
    url = models.URLField(blank=True,null=True)

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)    


from django.db import models
from django.core import validators

# Create your models here.
class Product(models.Model):
    id = models.BigAutoField(
        primary_key=True
    )

    name = models.CharField(
        max_length=70,
        verbose_name='Product Name',null=True,blank=True
    )

    description = models.TextField(
        max_length=800,
        verbose_name='Description'
    )

    price = models.FloatField(
        verbose_name='Price',
        validators=[
            validators.MinValueValidator(50),
            validators.MaxValueValidator(100000)
        ]
    )


class OrderDetail(models.Model):
    
    id = models.BigAutoField(
        primary_key=True
    )

    # You can change as a Foreign Key to the user model
    customer_email = models.EmailField(
        verbose_name='Customer Email'
    )

    product = models.ForeignKey(
        to=Product,
        verbose_name='Product',
        on_delete=models.PROTECT
    )

    amount = models.IntegerField(
        verbose_name='Amount'
    )

    stripe_payment_intent = models.CharField(
        max_length=200
    )

    # This field can be changed as status
    has_paid = models.BooleanField(
        default=False,
        verbose_name='Payment Status'
    )

    created_on = models.DateTimeField(
        auto_now_add=True
    )

    updated_on = models.DateTimeField(
        auto_now_add=True
    )