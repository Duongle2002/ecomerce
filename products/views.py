from django.shortcuts import get_object_or_404, render
from rest_framework import views
from rest_framework.response import Response
from django.http import Http404, JsonResponse
import cloudinary.uploader
from cart.models import Cart, CartItem
# from django.contrib.auth.models import User
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductImageSerializer,
    ProductCommentSerializer
)
from .models import Category, Product, ProductImage, ProductComment, productcarosel
from fruitables.helpers import custom_response, parse_request
from rest_framework.parsers import JSONParser
from json import JSONDecodeError
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()



def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        
        if product_id and quantity:
            product = Product.objects.get(id=product_id)
            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += int(quantity)
            cart_item.save()
            return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})




def all_products_view(request):
    # Lấy tất cả sản phẩm từ bảng Product
    products = Product.objects.all()
    carosel = productcarosel.objects.all()
    return render(request, 'product.html', {'products': products , 'carosel': carosel})

def filtered_products(request):
    category_id = request.GET.get('category')
    if category_id == 'all':
        products = Product.objects.all()
    elif category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()  # Mặc định hiển thị tất cả sản phẩm
    return render(request, 'filtered_products.html', {'products': products})

def product_detail(request, product_id):
    product_images = ProductImage.objects.filter(product_id=product_id)
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_details.html', {'product': product ,'product_images': product_images })




class CategoryAPIView(views.APIView):
    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return custom_response('Get all categories successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Get all categories failed!', 'Error', None, 400)

    def post(self, request):
        data = parse_request(request)
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return custom_response('Create category successfully!', 'Success', serializer.data, 201)
        else:
            return custom_response('Create category failed', 'Error', serializer.errors, 400)


class CategoryDetailAPIView(views.APIView):
    def get_object(self, id_slug):
        try:
            return Category.objects.get(id=id_slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, id_slug, format=None):
        try:
            category = self.get_object(id_slug)
            serializer = CategorySerializer(category)
            return custom_response('Get category successfully!', 'Success', serializer.data, 200)
        except Http404:
            return custom_response('Get category failed!', 'Error', "Category not found!", 400)

    def put(self, request, id_slug):
        try:
            data = parse_request(request)
            category = self.get_object(id_slug)
            serializer = CategorySerializer(category, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update category successfully!', 'Success', serializer.data, 200)
            else:
                return custom_response('Update category failed', 'Error', serializer.errors, 400)
        except Http404:
            return custom_response('Update category failed', 'Error', "Category not found!", 400)

    def delete(self, request, id_slug):
        try:
            category = self.get_object(id_slug)
            category.delete()
            return custom_response('Delete category successfully!', 'Success', {"category_id": id_slug}, 204)
        except Http404:
            return custom_response('Delete category failed!', 'Error', "Category not found!", 400)

class ProductViewAPI(views.APIView):
    def get(self, request):
        try:
            products = Product.objects.all()
            serializers = ProductSerializer(products, many=True)
            return custom_response('Get all products successfully!', 'Success', serializers.data, 200)
        except:
            return custom_response('Get all products failed!', 'Error', None, 400)

    def post(self, request):
        try:
            product_data_list = request.data
            created_products = []
            for product_data in product_data_list:
                category = Category.objects.get(id=product_data['category_id'])
                product = Product.objects.create(
                    name=product_data['name'],
                    unit=product_data['unit'],
                    detail=product_data.get('detail', None),
                    price=product_data['price'],
                    discount=product_data['discount'],
                    amount=product_data['amount'],
                    thumbnail=product_data['thumbnail'],
                    category_id=category
                )
                created_products.append(product)
            
            serializer = ProductSerializer(created_products, many=True)
            return custom_response('Create products successfully!', 'Success', serializer.data, 201)
        except Exception as e:
            return custom_response('Create products failed', 'Error', {"error": str(e)}, 400)

class ProductDetailAPIView(views.APIView):
    def get_object(self, id_slug):
        try:
            return Product.objects.get(id=id_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id_slug, format=None):
        try:
            product = self.get_object(id_slug)
            serializer = ProductSerializer(product)
            return custom_response('Get product successfully!', 'Success', serializer.data, 200)
        except Product.DoesNotExist:
            return custom_response('Get product failed!', 'Error', "Product not found!", 400)

    def put(self, request, id_slug):
        try:
            product = self.get_object(id_slug)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update product successfully!', 'Success', serializer.data, 200)
            else:
                return custom_response('Update product failed', 'Error', serializer.errors, 400)
        except Product.DoesNotExist:
            return custom_response('Update product failed', 'Error', "Product not found!", 400)

    def delete(self, request, id_slug):
        try:
            product = self.get_object(id_slug)
            product.delete()
            return custom_response('Delete product successfully!', 'Success', {"product_id": id_slug}, 204)
        except Product.DoesNotExist:
            return custom_response('Delete product failed!', 'Error', "Product not found!", 400)

class ProductImageAPIView(views.APIView):
    def get(self, request, product_id_slug):
        try:
            product_images = ProductImage.objects.filter(
                product_id=product_id_slug).all()
            serializers = ProductImageSerializer(product_images, many=True)
            return custom_response('Get all product images successfully!', 'Success', serializers.data, 200)
        except:
            return custom_response('Get all product images failed!', 'Error', 'Product images not found', 400)

    def post(self, request, product_id_slug):
        try:
            if 'uploadImages' not in request.FILES:
                return custom_response('No upload resource', 'Error', 'No image file found in request', 400)

            images = request.FILES.getlist('uploadImages')
            data = []
            for image in images:
                try:
                    upload_result = cloudinary.uploader.upload(image)
                    # Lấy đối tượng Product từ id
                    product = Product.objects.get(id=product_id_slug)
                    # Tạo một đối tượng ProductImage với product_id là instance của Product
                    product_image = ProductImage.objects.create(
                        product_id=product,
                        image_url=upload_result['secure_url'],  # Sử dụng secure_url của kết quả upload
                    )
                    serializer = ProductImageSerializer(product_image)
                    data.append(serializer.data)
                except Exception as e:
                    return custom_response('Upload images failed!', 'Error', str(e), 400)

            return custom_response('Upload images successfully!', 'Success', data, 200)
        except Exception as e:
            return custom_response('Create product image failed', 'Error', {"error": str(e)}, 400)
        
class ProductImageDetailAPIView(views.APIView):
    def get_object(self, id_slug):
        try:
            return ProductImage.objects.get(id=id_slug)
        except:
            raise Http404

    def get_object_with_product_id(self, product_id_slug, id_slug):
        try:
            return ProductImage.objects.get(product_id=product_id_slug, id=id_slug)
        except:
            raise Http404

    def get(self, request, product_id_slug, id_slug, format=None):
        try:
            product_image = self.get_object(id_slug)
            serializer = ProductImageSerializer(product_image)
            return custom_response('Get product image successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Get product image failed!', 'Error', "Product image not found!", 400)

    def put(self, request, product_id_slug, id_slug):
        try:
            data = parse_request(request)
            product_image = self.get_object_with_product_id(
                product_id_slug, id_slug)
            serializer = ProductImageSerializer(product_image, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update product image successfully!', 'Success', serializer.data, 200)
            else:
                return custom_response('Update product image failed', 'Error', serializer.errors, 400)
        except:
            return custom_response('Update product image failed', 'Error', "Product image not found!", 400)

    def delete(self, request, product_id_slug, id_slug):
        try:
            product_image = self.get_object_with_product_id(
                product_id_slug, id_slug)
            product_image.delete()
            return custom_response('Delete product image successfully!', 'Success', {"product_image_id": id_slug}, 204)
        except:
            return custom_response('Delete product image failed!', 'Error', "Product image not found!", 400)


class ProductCommentAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, product_id_slug):
        try:
            product_comments = ProductComment.objects.filter(
                product_id=product_id_slug).all()
            serializers = ProductCommentSerializer(product_comments, many=True)
            return custom_response('Get all product comments successfully!', 'Success', serializers.data, 200)
        except:
            return custom_response('Get all product comments failed!', 'Error', None, 400)

    def post(self, request, product_id_slug):
        try:
            data = parse_request(request)
            product = Product.objects.get(id=data['product_id'])
            # Giống code cũ nhưng import khác nhé
            user = User.objects.get(id=data['user_id'])
            product_comment = ProductComment(
                product_id=product,
                rating=data['rating'],
                comment=data['comment'],
                user_id=user,
                parent_id=data['parent_id']
            )
            product_comment.save()
            serializer = ProductCommentSerializer(product_comment)
            return custom_response('Create product comment successfully!', 'Success', serializer.data, 201)
        except Exception as e:
            return custom_response('Create product comment failed', 'Error', [str(e)], 400)


class ProductCommentDetailAPIView(views.APIView):
    def get_object(self, id_slug):
        try:
            return ProductComment.objects.get(id=id_slug)
        except:
            raise Http404

    def get_object_with_product_id(self, product_id_slug, id_slug):
        try:
            return ProductComment.objects.get(product_id=product_id_slug, id=id_slug)
        except:
            raise Http404

    def get(self, request, product_id_slug, id_slug, format=None):
        try:
            product_comment = self.get_object(id_slug)
            serializer = ProductCommentSerializer(product_comment)
            return custom_response('Get product comment successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Get product comment failed!', 'Error', "Product comment not found!", 400)

    def put(self, request, product_id_slug, id_slug):
        try:
            data = parse_request(request)
            product_comment = self.get_object_with_product_id(
                product_id_slug, id_slug)
            serializer = ProductCommentSerializer(product_comment, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update product comment successfully!', 'Success', serializer.data, 200)
            else:
                return custom_response('Update product comment failed', 'Error', serializer.errors, 400)
        except:
            return custom_response('Update product comment failed', 'Error', "Product comment not found!", 400)

    def delete(self, request, product_id_slug, id_slug):
        try:
            product_comment = self.get_object_with_product_id(
                product_id_slug, id_slug)
            product_comment.delete()
            return custom_response('Delete product comment successfully!', 'Success', {"product_comment_id": id_slug}, 204)
        except:
            return custom_response('Delete product comment failed!', 'Error', "Product comment not found!", 400)
