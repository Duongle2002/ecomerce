from django.shortcuts import render
from homeapp.models import homeimg, upset
from products.models import Product

def home(request):
    images = homeimg.objects.all()
    upsets = upset.objects.all()
    popular_products = Product.objects.filter(is_public=True)[:5]

    # Lấy các sản phẩm thuộc danh mục "Ưa mát"
    mini_desktop_plants = Product.objects.filter(category_id__name='Ưa mát')[:4]
    mini_desktop_plant = Product.objects.filter(category_id__name='Ưa mát').first()


    # Lấy sản phẩm banner cho danh mục "Ít nắng" và các sản phẩm trong danh mục đó
    indoor_plant_banner = Product.objects.filter(category_id__name='Ít nắng').first()
    indoor_plants = Product.objects.filter(category_id__name='Ít nắng')[:8]

    context = {
        'images': images,
        'upsets': upsets,
        'popular_products': popular_products,
        'mini_desktop_plants': mini_desktop_plants,
        'mini_desktop_plant': mini_desktop_plant,
        'indoor_plants': indoor_plants,
        'indoor_plant_banner': indoor_plant_banner,
    }
    return render(request, 'home.html', context)
