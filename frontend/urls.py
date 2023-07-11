from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path("about", views.about, name="about"),
    path("emission_evaluator", views.emission_evaluator, name="emission_evaluator"),
    # API
    path('get_center_details/', views.get_center_details, name='get_center_details'),
    path('get_product_group_details/', views.get_product_group_details, name='get_product_group_details'),
    path('product-groups/', views.product_groups, name='product_groups'),
    path('product-data/<int:product_id>/', views.product_data, name='product_data'),
]


