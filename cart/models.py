from django.db import models
from accounts.models import ShopUser
from django.utils.translation import gettext_lazy as _
from productsMaintain.models import Product, Size
from localflavor.us.models import USPostalCodeField
from django.utils import timezone

class Order(models.Model):
    user = models.ForeignKey(ShopUser,
                             related_name='orders',
                             on_delete=models.CASCADE)

    created = models.DateTimeField(_('Created time'), auto_now_add=True,
                                   editable=False,
                                   blank=False)
    payTime = models.DateTimeField(_('Payment time'),
                                   default=timezone.now)

    paid = models.BooleanField(_('Paid'), default=False)
    braintreeId = models.CharField(max_length=200, blank=True)


    deliveredToAnotherAddress = models.BooleanField(_('Delive to another address'),
                                                    blank=False,
                                                    default=False)
    #if yes, delivery details
    #D like delivery

    firstNameD = models.CharField(_('first name'), max_length=30,
                                 blank=True)
    lastNameD = models.CharField(_('Last name'), max_length=30,
                                blank=True)
    addressD = models.CharField(_('Address'), max_length=100,
                               blank=True)
    cityD = models.CharField(_('City'), max_length=40,
                            blank=True)
    zipCodeD = USPostalCodeField(_('Zip code'), blank=True)
    telephoneNumberD = models.CharField(_('Telephone number'),
                                       max_length=12,
                                       blank=True)
    extraInfoD = models.TextField(_('Extra information'), blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return str(self.id)

    @property
    def orderCost(self):
        objects = OrderItem.objects.filter(order=self)
        total_cost = 0
        for item in objects:
            total_cost += item.productCost
        return total_cost

    def __iter__(self):
        objects = OrderItem.objects.filter(order=self)
        for single in objects:
            yield single


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='orderedItems',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='orderWrappers',
                                on_delete=models.CASCADE)
    size = models.ForeignKey(Size,
                             related_name='ordersWithThisSize',
                             on_delete=models.CASCADE)

    quantity = models.IntegerField(_('Quantity'), blank=False)
    costPerItem = models.DecimalField(_('Cost per item'),
                                      blank=False, default=0.00,
                                      max_digits=8,
                                      decimal_places=2)

    @property
    def productCost(self):
        return self.costPerItem*self.quantity

    def __str__(self):
        return str(self.product)+' '+str(self.size)

