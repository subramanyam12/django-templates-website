from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES=(
    ('CD','Curd'),
    ('ML','Milk'),
    ('LS','Lassi'),
    ('MK','Milkshake'),
    ('PN','panner'),
    ('GH','Ghee'),
    ('CZ','Cheese'),
    ('IC','Ice-Cream')
) 

STATE_CHOICES=(
    ('ANDHRA PRADESH','ANDHRA PRADESH'),
    ('TELANGANA','TELANGANA'),
    ('TAMILNADU','TAMILNADU'),
    ('KERALA','KERALA'),
    ('KARNATAKA','KARNATAKA')
)

# Create your models here.
class Product(models.Model):
    title=models.CharField(max_length=50)
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    description=models.TextField()
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image=models.ImageField(upload_to="product")
    def __str__(self):
        return self.title


class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    mobile=models.IntegerField(default=0)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=100)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price

class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.FloatField()
    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
    paid=models.BooleanField(default=False)
    
STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,default='')
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,default='')

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price


class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
 