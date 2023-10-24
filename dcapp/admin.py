from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.urls import reverse

# from django.contrib.auth.models import Group
# admin.site.unregister(Group)
 

admin.site.site_header='Siddu Products'
admin.site.site_title='Siddu Products'
admin.site.site_index_title='Welcome to Siddu Dairy Products'
#Register your models here

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','title','discount_price','category','product_image']

@admin.register(Customer)
class Customer(admin.ModelAdmin):
    list_display=['id','user','locality','city','state','zipcode']

@admin.register(Cart)
class Cart(admin.ModelAdmin):
    list_display=['id','user','products','quantity']
    def products(self,obj):
        link=reverse('admin:dcapp_product_change',args=[obj.product.pk])
        return format_html("<a href='{}'>{}</a>",link,obj.product.title)

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display=['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class OrderPlaced(admin.ModelAdmin):
    list_display=['user','customer','product','quantity','ordered_date','status','payment']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display=['id','user','product'] 