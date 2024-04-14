from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from .forms import UserRegistrationForm
from rest_framework.permissions import IsAuthenticated
from fruitables.helpers import custom_response
from user.serializers import UserAccountSerializer, UserAccountUpdateSerializer
from rest_framework import views
from django.contrib.auth.decorators import login_required

class UserAccountUpdateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserAccountSerializer(request.user)
        return custom_response('Get user successfully!', 'Success', serializer.data, 200)

    def put(self, request, *args, **kwargs):
        serializer = UserAccountUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return custom_response('Update user successfully!', 'Success', serializer.data, 200)
        return custom_response('Update user failed!', 'Error', serializer.errors, 400)


# views.py

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect("homeapp:homeapps")
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('users:login')  # Chuyển hướng người dùng đến trang đăng nhập sau khi đăng xuất

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            form.save()
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                # Chuyển hướng người dùng đến trang đăng nhập sau khi đăng ký thành công
                return redirect('users:login') 
            
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form} )

