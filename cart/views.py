from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from .forms import CartChangeQuantity
from django.views.decorators.http import require_POST
from productsMaintain.models import Product


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
    #todo: print message that you deleted product
    return redirect('cart:myCart')

@require_POST
def CartUpdate(request, productSlug, sizeId):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=productSlug)
    form = CartChangeQuantity(request.POST)

    if form.is_valid():
        newQuantity = form.cleaned_data['quantity']
        cart.addProduct(product, newQuantity, sizeId, update=True)
    # todo: print message that you changed quantity
    return redirect('cart:myCart')

