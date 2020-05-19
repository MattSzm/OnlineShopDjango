from django.urls import path
from . import views


urlpatterns = [
    path('list/', views.ProductListView.as_view(),
         name='product_list'),
    path('list/<slug:category_slug>/',
         views.ProductListView.as_view(),
         name='product_list_for_category')
]