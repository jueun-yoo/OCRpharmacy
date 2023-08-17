from django.urls import path
from . import views
from .views import login_view, logout_view

app_name = 'user'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', login_view, name='login'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('logout/', logout_view, name='logout'),
    path('', views.root_redirect, name='root_redirect'),  # 루트 URL에서 root_redirect 뷰를 연결
]
