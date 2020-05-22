from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views


urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'), name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(
        template_name='registration/logged.html'
    ), name='logout'),
    path('accounts/register/', accounts_views.register, name='register' ),
    path('products/', include('productsMaintain.urls')),
    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)