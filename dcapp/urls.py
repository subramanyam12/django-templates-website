from django.urls import path
from .views import *

from django.contrib.auth import views as auth_view
urlpatterns = [
    # path('index',index,name='home'),
    path('',home,name='home'),
    path('about',about,name='about'),
    path('contact',contact,name='contact'),
    path('category/<slug:val>',category.as_view(),name='category'),
    path('category-title/<val>',categorytitle,name='category-title'),
    path('productdetail/<int:pk>',productdetail,name='product-detail'),
    path('profile',profile.as_view(),name='profile'),
    path('address',address,name='address'),
    path('updateaddress/<int:pk>',address_update.as_view(),name='updateaddress'),
       
    path('add-to-cart/',add_to_cart,name='add-to-cart'),
    path('cart/',show_cart,name='showcart'),
    path('checkout/',checkout.as_view(),name='checkout'),
    path('pluscart/',plus_cart),
    path('minuscart/',minus_cart),
    path('removecart/',remove_cart),
    path('pluswishlist/',plus_wishlist),
    path('minuswishlist/',minus_wishlist),
    
    path('paymentdone/',payment_done,name='paymentdone'),
    path('orders/',orders,name='orders'),

    path('search/',search,name='search'),

    


    #Login
    path('register/',register.as_view(),name='register'),
    path('accounts/login/',auth_view.LoginView.as_view(template_name='login.html',authentication_form=LoginForm),name='login'),
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone'),name='passwordchange'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),name='passwordchangedone'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),

    path('password_reset/',auth_view.PasswordResetView.as_view(template_name='password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password_reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password_reset_complete/',auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
    
    
    
]

