from django.urls import path
from introduce import views

app_name = 'introduce'
urlpatterns =[
    path ("" , views.introduce, name="introduces"),
    path ("contacts/" , views.contact, name="contacts"),
    
]