from django.urls import path
from . import views
app_name = 'supplements'

urlpatterns = [
    path('supplement/<int:supplement_id>/', views.supplement_detail, name='supplement_detail'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('process_image', views.process_image, name='process_image'),
    path('save_info/', views.save_info, name='save_info')
]