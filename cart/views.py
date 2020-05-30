from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from .forms import CartChangeQuantity, OrderForm
from django.views.decorators.http import require_POST
from productsMaintain.models import Product
from django.views.generic.base import TemplateResponseMixin, View
from . import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


def CartDetail(request):
    cart = Cart(request)
    for item in cart:
        item['changeQuantityForm'] = CartChangeQuantity(
            initial={'quantity': item['quantity'],})
    return render(request, 'cart/cartDetail.html',
                  {'cart': cart,})

def CartRemove(request, productSlug, sizeId):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=productSlug)

    cart.removeProduct(product, sizeId)
    messages.info(request, 'You have removed the product.')
    return redirect('cart:cartDetail')

@require_POST
def CartUpdate(request, productSlug, sizeId):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=productSlug)
    form = CartChangeQuantity(request.POST)
    if form.is_valid():
        newQuantity = form.cleaned_data['quantity']
        cart.addProduct(product, newQuantity, sizeId, update=True)
    messages.info(request, 'You have changed the quantity.')
    return redirect('cart:cartDetail')


class OrderView(TemplateResponseMixin, View):
    model = models.Order
    template_name = 'order/createOrder.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('%s?next=%s' % (reverse('accounts:login'),
                                                reverse('cart:createOrder')))


        canBeDelivered = request.user.CanBeDelivered
        form = OrderForm(initial={'deliveredToAnotherAddress': False})

        return self.render_to_response({'canBeDelivered': canBeDelivered,
                                        'form': form})

    def post(self, request):
        cart = Cart(request)
        form  = OrderForm(request.POST)
        if form.is_valid():
            cleanData = form.cleaned_data
            if ((cleanData['deliveredToAnotherAddress'] == False
                    and request.user.CanBeDelivered) or
                (cleanData['deliveredToAnotherAddress'] == True and
                 (cleanData['firstNameD'] and cleanData['lastNameD'] and
                 cleanData['addressD'] and cleanData['cityD'] and
                 cleanData['zipCodeD'] and cleanData['telephoneNumberD']))):

                order = form.save(commit=False)
                order.user = request.user
                order.save()
                for item in cart:
                    models.OrderItem.objects.create(order=order,
                                                    product=item['productObject'],
                                                    size=item['size'],
                                                    quantity=item['quantity'],
                                                    costPerItem =
                                                        item['productObject'].price)
                cart.clear()
                #using in payment!
                request.session['orderId'] = order.id
                #return redirect(reverse('payment................'))
                return redirect(reverse('accounts:dashboard'))
            else:
                messages.error(request, 'Complete all necessary fields.')
        else:
            messages.error(request, 'You need to complete all fields in proper way.')
        return redirect(reverse('cart:createOrder'))