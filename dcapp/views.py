from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.views import View
from .models import *
from .forms import *
import razorpay
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
# def index(request):
#     return render(request,'index.html')
@login_required
def home(request):
    totalitem=0
    wishlist=0
    if request.user.is_authenticated: 
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlist=len(Wishlist.objects.filter(user=request.user))
    return render(request,'home.html',locals())

def about(request):
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlist=len(Wishlist.objects.filter(user=request.user))
    return render(request,'about.html',locals())

def contact(request):
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlist=len(Wishlist.objects.filter(user=request.user))
    return render(request,'contact.html',locals())

@method_decorator(login_required,name='dispatch')
class category(View):
    def get(self,request,val):
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishlist=len(Wishlist.objects.filter(user=request.user))
        product=Product.objects.filter(category=val)
        titles=Product.objects.filter(category=val).values('title')
        return render(request,'category.html',locals())

def categorytitle(request,val):
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlist=len(Wishlist.objects.filter(user=request.user))
    product=Product.objects.filter(title=val)
    titles=Product.objects.filter(category=product[0].category).values('title')
    return render(request,'category.html',locals())

def productdetail(request,pk):
    product=Product.objects.get(pk=pk)
    wishlist=Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
    totalitem=0
    # wishlist=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        # wishlist=len(Wishlist.objects.filter(user=request.user))
    return render(request,'productdetail.html',locals())

   
    
class register(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishlist=len(Wishlist.objects.filter(user=request.user))
        return render(request,'register.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratulations! User Register Suceesfully')
        else:
            messages.warning(request,"Invalid Input data")
        return render(request,'register.html',locals())

# class Login(View):
#     def get(self,request):
#         return render(request,'login.html')
#     def post(self,request):
#         username=request.POST['username']
#         password=request.POST['password']
#         data=authenticate(username=username,password=password)
#         if data is not None:
#             login(request,data)
#             messages.success(request,'Suceesfully logged In')
#             return redirect('profile')
#         else:
#             messages.error(request,"Invalid Credentials")
#         return render(request,'login.html',locals())

class profile(View):
    def get(self,request):
        form=CustomerForm()
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
             totalitem=len(Cart.objects.filter(user=request.user))
             wishlist=len(Wishlist.objects.filter(user=request.user))
        return render(request,'profile.html',locals())
    def post(self,request):
        form=CustomerForm(request.POST)
        if form.is_valid():
            user =request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            
            reg=Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulations Profile Save Successfully')
        else:
            messages.warning(request,'Invlaid Input Data')
        return render(request,'profile.html',locals())




def address(request):
    add =Customer.objects.filter(user=request.user)
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlist=len(Wishlist.objects.filter(user=request.user))
    return render(request,'address.html',locals())

class address_update(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerForm(instance=add)
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishlist=len(Wishlist.objects.filter(user=request.user))
        return render(request,'updateaddress.html',locals())
    def post(self,request,pk):
        form=CustomerForm(request.POST)
        if form.is_valid():
            add =Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,'Congratulations Profile Update Successfully')
        else:
            messages.warning(request,'Invlaid Input Data')
        return redirect('address')

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity * p.product.discount_price
        amount=amount + value
    totalamount = amount + 40
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlist=len(Wishlist.objects.filter(user=request.user))
    return render(request,'addtocart.html',locals())


def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart =Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity * p.product.discount_price
            amount=amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
             'amount':amount,
             'totalamount':totalamount
        }
    return JsonResponse(data)

def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart =Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity * p.product.discount_price
            amount=amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
             'amount':amount,
             'totalamount':totalamount
        }
    return JsonResponse(data)

def remove_cart(request):
    if request.method=='GET':
        product_id=request.GET['product_id']
        c=Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.delete()
        user=request.user
        cart =Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity * p.product.discount_price
            amount=amount + value
        totalamount = amount + 40
        data={
             'amount':amount,
             'totalamount':totalamount
        }
    return JsonResponse(data)

def plus_wishlist(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user=request.user
        Wishlist(user=user,product=product).save()
        data={
            'message':'Wishlist Added Successfully'
        }
    return JsonResponse(data)

def minus_wishlist(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user=request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data={
            'message':'Wishlist Remove Successfully'
        }
    return JsonResponse(data)
class checkout(View):
    def get(self,request):
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishlist=len(Wishlist.objects.filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value=p.quantity * p.product.discount_price
            famount=famount + value
        totalamount = famount + 40
        razoramount=int(totalamount * 100)
        client=razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data={'amount':razoramount,'currency':'INR',"receipt":'order_rcptid_12'}
        payment_response=client.order.create(data=data)
        print(payment_response)
        order_id=payment_response['id']
        order_status=payment_response['status']
        if order_status=='created':
            payment=Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
        return render(request,'checkout.html',locals())
    
def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    user=request.user
    customer=Customer.objects.get(id=cust_id)
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid=True
    payment.razorpay_payment_id=payment_id
    payment.save()
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
            
            c.delete()
    return redirect('orders')

def orders(request):
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request,'orders.html',locals())

def search(request):
    query=request.GET['search']
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlist=len(Wishlist.objects.filter(user=request.user))
    product=Product.objects.filter(Q(title__icontains=query))
    return render(request,'search.html',locals())
    


    
    
