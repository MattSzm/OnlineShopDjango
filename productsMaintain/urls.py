from django.urls import path
from . import views


urlpatterns = [
    path('list/', views.ProductListView.as_view(),
         name='product_list'),
    path('list/<slug:category_slug>/',
         views.ProductListView.as_view(),
         name='product_list_for_category'),
    path('<slug:category_slug>/detail/<slug:product_slug>/',
         views.ProductDetailView.as_view(),
         name='product_detail_view'),
    path('<slug:category_slug>/detail/<slug:product_slug>/<int:id_image>/',
         views.ProductDetailView.as_view(),
         name='product_detail_view_diff_image'),
    path('list/brand/<slug:brand_slug>/',
         views.BrandListView.as_view(),
         name='product_list_for_brand'),
    path('list/brand/<slug:brand_slug>/<slug:category_slug>/',
         views.BrandListView.as_view(),
         name='product_list_for_brand_and_category'),
]
