from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('submit_order/', views.submit_orders, name='submit_order'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
]
