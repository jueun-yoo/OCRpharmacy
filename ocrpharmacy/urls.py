from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('',RedirectView.as_view(pattern_name='accounts'), name='home'),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('supplements/', include('supplements.urls')),
    path('accounts/',include('accounts.urls')),
]
