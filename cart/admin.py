from django.contrib import admin
from . import models

class OrderItemLine(admin.TabularInline):
    model = models.OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','created','payTime','paid',
                    'braintreeId',
                    'deliveredToAnotherAddress']
    inlines = [OrderItemLine]

admin.site.register(models.Order, OrderAdmin)