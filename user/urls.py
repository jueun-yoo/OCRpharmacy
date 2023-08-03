from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    # ... 다른 URL 패턴 ...
    path('signup/', views.signup_view, name='signup'),
]
