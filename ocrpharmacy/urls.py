from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('supplements/', include('supplements.urls')),
    
]
