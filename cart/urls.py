from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartDetail, name = 'cartDetail'),
    path('remove/<slug:productSlug>/<int:sizeId>/',
         views.CartRemove, name = 'cartRemove'),
    path('update/<slug:productSlug>/<int:sizeId>/',
         views.CartUpdate, name= 'cartUpdate'),
    path('order/create/', views.OrderView.as_view(),
         name = 'createOrder'),
    path('payment/', views.payment.as_view(),
         name = 'payment'),
    path('payment/<int:id>/rejected', views.paymentRejected,
         name = 'paymentRejected'),
    path('createpdf/<int:OrderId>/', views.createPdf,
         name = 'createPdf'),
]