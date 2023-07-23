from django.urls import path

from accounts import views

urlpatterns =[
    path('',views.sign_up,name='sign_up'),
]