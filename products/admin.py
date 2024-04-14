from django.contrib import admin
admin.ModelAdmin.search_fields = ('email',)
from .models import Category, Product, ProductImage, ProductComment, productcarosel

# Đăng ký các model của bạn với trang admin
class Categorys(admin.ModelAdmin):
    list_display = [ "id","name"]
    search_fields = ["name"]
admin.site.register(Category ,Categorys)

class Products(admin.ModelAdmin):
    list_display = ["name" ,"id"]
    search_fields = ["name"]
admin.site.register(Product,Products)

class ProductImages(admin.ModelAdmin):
    list_display = ["product_id" ,"id"]
    search_fields = ["product_id"]
admin.site.register(ProductImage,ProductImages)

admin.site.register(ProductComment )

class productcarosels(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
admin.site.register(productcarosel,productcarosels)
