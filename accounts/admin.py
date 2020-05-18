from django.contrib import admin
from .models import ShopUser

@admin.register(ShopUser)
class ShopUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'firstName', 'lastName', 'is_staff','dataJoined']
    ordering = ('email',)
