from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from productsMaintain.views import MainPange


urlpatterns = [
    path('account/', include('accounts.urls', namespace='accounts')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('products/', include('productsMaintain.urls')),
    path('admin/', admin.site.urls),
    path('', MainPange, name='mainPage')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)