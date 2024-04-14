
from .models import CartItem

def cart_items(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart__user=request.user)
    else:
        cart_items = []
    return {'cart_items': cart_items}
