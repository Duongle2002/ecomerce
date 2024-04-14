from django.shortcuts import render
from cart.models import CartItem
from homeapp.models import homeimg, upset
from django.urls import reverse

from products.models import Product

def home(request):
    images = homeimg.objects.all()
    upsets = upset.objects.all()
    logout_url = reverse('users:logout')  # Tạo URL của logout từ ứng dụng user
    
    popular_products = Product.objects.filter(is_public=True)[:5]

    # Lấy các sản phẩm thuộc danh mục "Ưa mát"
    mini_desktop_plants = Product.objects.filter(category_id__name='Ưa mát')[:4]

    # Lấy sản phẩm banner cho danh mục "Ưa mát"
    mini_desktop_plant = Product.objects.filter(category_id__name='Ưa mát').first()

    # Lấy sản phẩm banner cho danh mục "Ít nắng"
    indoor_plant_banner = Product.objects.filter(category_id__name='Ít nắng').first()

    # Lấy các sản phẩm thuộc danh mục "Ít nắng"
    indoor_plants = Product.objects.filter(category_id__name='Ít nắng')[:8]
    return render(request, 'home.html', {'images': images,
                                            'upsets': upsets, 
                                            'logout_url': logout_url ,
                                            'popular_products': popular_products,
                                            'mini_desktop_plants': mini_desktop_plants,
                                            'mini_desktop_plant': mini_desktop_plant,
                                            'indoor_plants': indoor_plants,
                                            'indoor_plant_banner': indoor_plant_banner,})

