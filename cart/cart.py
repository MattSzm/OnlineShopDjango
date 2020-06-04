from decimal import Decimal
from django.conf import settings
from productsMaintain import models

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart  = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = {}
            self.session[settings.CART_SESSION_ID] = cart
        self.cart = cart

    def addProduct(self, product, quantity, sizeId, update=False):
        productId = product.id
        fullName = self.createFullName(productId, sizeId)

        if not fullName in self.cart:
            self.cart[fullName] = {'quantity': 0,}

        if update:
            self.cart[fullName]['quantity'] = quantity
        else:
            self.cart[fullName]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def removeProduct(self, product, sizeId):
        productId = product.id
        fullName = self.createFullName(productId, sizeId)
        if fullName in self.cart:
            del self.cart[fullName]
            self.save()

    def __iter__(self):
        #before I realized I need to carry about sizes
        """productsIds = []
        for key in self.cart.keys():
            item = str(key).rsplit('.',1)[0]
            productsIds.append(item)
        products = models.Product.objects.filter(id__in=productsIds)"""

        cartCopy = self.cart.copy()
        for key in cartCopy:
            productId = str(key).rsplit('.',1)[0]
            sizeId = str(key).rsplit('.',1)[1]

            product = models.Product.objects.get(id=int(productId))
            size = models.Size.objects.get(id=int(sizeId))

            cartCopy[key]['productObject'] = product
            cartCopy[key]['wholePrice'] = product.currentPrice*\
                                          cartCopy[key]['quantity']
            cartCopy[key]['size'] = size
            yield cartCopy[key]

    def cartCapacity(self):
        count = 0
        for value in self.cart.values():
            count += value['quantity']
        return count

    def cartTotalCost(self):
        totalPrice = 0
        for key in self.cart:
            productId = str(key).rsplit('.', 1)[0]
            totalPrice += models.Product.objects.get(
                id=int(productId)).currentPrice *\
                          self.cart[key]['quantity']
        return totalPrice

    @property
    def shipCost(self):
        return Decimal(10.00)

    def cartTotalCostWithShip(self):
        return self.cartTotalCost() + self.shipCost

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def createFullName(self, productId, sizeId):
        return str(productId) + '.' + str(sizeId)

    @property
    def isEmpty(self):
        if len(self.cart) == 0:
            return True
        return False
