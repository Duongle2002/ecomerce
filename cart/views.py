from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse

from cart.forms import OrderForm

from .models import Cart, CartItem, OrderedItem, Orders
from products.models import Product
import json
from django.db.models import Sum

from decimal import Decimal  

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity')
            
            # Truy xuất sản phẩm và kiểm tra xem nó có tồn tại không
            product = get_object_or_404(Product, pk=product_id)
            
            # Đảm bảo số lượng là một số nguyên dương
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Số lượng phải là một số nguyên dương.")
            
            # Tính tổng giá cho số lượng sản phẩm
            total_price = product.price * quantity
            
            # Truy xuất hoặc tạo giỏ hàng của người dùng
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Tạo hoặc cập nhật mục giỏ hàng
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity = quantity  # Cập nhật lại số lượng
                cart_item.total_price = total_price  # Cập nhật lại tổng giá
                cart_item.save()
            else:
                cart_item.quantity = quantity
                cart_item.total_price = total_price
                cart_item.save()
            
            return JsonResponse({'message': 'Thêm sản phẩm vào giỏ hàng thành công'}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Sản phẩm không tồn tại'}, status=404)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Phương thức không được phép'}, status=405)



@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = cart_items.aggregate(total_price=Sum('total_price'))['total_price']
    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart:view_cart')
def checkout(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = cart_items.aggregate(total_price=Sum('total_price'))['total_price']
    return render(request,'checkouts.html', {'cart_items': cart_items, 'total_price': total_price})

def submit_orders(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            cart_items = CartItem.objects.filter(cart__user=request.user)
            for cart_item in cart_items:
                OrderedItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            cart_items.delete()
            ordered_items = order.ordereditem_set.all()  # Lấy ra các sản phẩm đã mua
            total_price = sum(item.price for item in ordered_items)  # Tính tổng giá trị của đơn hàng
            return render(request, 'payment_receipt.html', {'order': order, 'ordered_items': ordered_items, 'total_price': total_price})
    else:
        form = OrderForm()
    return render(request, 'payment_form.html', {'form': form})

def order_detail(request, order_id):
    order = Orders.objects.get(id=order_id)
    return render(request, 'order_detail.html', {'order': order})