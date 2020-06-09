from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from .forms import CartChangeQuantity, OrderForm
from django.views.decorators.http import require_POST
from productsMaintain.models import Product
from django.views.generic.base import TemplateResponseMixin, View
from . import models
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.contrib import messages
import braintree
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from accounts.recommendationSystem import RecommendationEngine


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
        recommendation = RecommendationEngine(request)
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
                                                        item['productObject'].currentPrice)
                    recommendation.removeSingle(item['productObject'].id)

                cart.clear()
                request.session['orderId'] = order.id
                return redirect(reverse('cart:payment'))
            else:
                messages.error(request, 'Complete all necessary fields.')
        else:
            messages.error(request, 'You need to complete all fields in proper way.')
        return redirect(reverse('cart:createOrder'))


class payment(TemplateResponseMixin, View):
    template_name = 'payment/app.html'
    order = None

    def dispatch(self, request, *args, **kwargs):
        self.order = get_object_or_404(models.Order,
                                       id = request.session['orderId'])
        return super(payment, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        token = braintree.ClientToken.generate()
        return self.render_to_response({'token': token,
                                        'order': self.order})

    def post(self, request):
        nonceKey = request.POST.get('payment_method_nonce')
        result = braintree.Transaction.sale({
            'purchase_order_number': '{}'.format(self.order.id),
            'amount': '{:.2f}'.format(self.order.orderCost),
            'shipping_amount': '10.00',
            'payment_method_nonce': nonceKey,
            'merchant_account_id': 'onlineShop',
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            self.order.payTime = timezone.now()
            self.order.paid = True
            self.order.braintreeId = result.transaction.id
            self.order.save()

            short_name = request.user.email.split('@')[0]
            title = 'Thank you {} for shopping'.format(short_name)
            body = "We accapted your order number:{}." \
                   "we will try to deliver it as soon as possible.\n\n" \
                   "OnlineShop Team".format(self.order.id)
            send_mail(title, body, settings.EMAIL_HOST_USER,
                      [request.user.email])

            messages.success(request, 'Your payment has been approved')
            return redirect(reverse('accounts:dashboard'))
        return redirect(reverse('cart:paymentRejected',
                                args=(self.order.id,)))

def paymentRejected(request, id):
    text = 'Order number:{} rejected.'.format(id)
    return render(request, 'payment/rejected.html',
                  {'text': text})


def createPdf(request, OrderId):
    order = get_object_or_404(models.Order,
                              id=OrderId)
    if order.user == request.user:
        response = HttpResponse(content_type='print/pdf')

        response['Content-Disposition'] = \
            'attachment; filename="Invoice_{}.pdf"'.format(OrderId)

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        p.setFont("Helvetica", 20, leading=None)
        p.setFillColorRGB(0,0,0)
        p.drawString(240,800,'Online Shop')
        p.line(0,780,1000,780)
        p.setFont("Helvetica", 18, leading=None)
        p.drawString(240, 730, 'Invoice no.{}'.format(OrderId))

        x=30
        y=690
        p.setFont("Helvetica", 15, leading=None)
        p.drawString(x,y,'Buyer:')
        p.drawString(x+400, y, 'Date of purchase:')
        p.drawString(x + 400, y-38, 'Date of Payement:')
        p.setFont("Helvetica", 12, leading=None)
        p.drawString(x + 400, y-18, '{}'.format(order.created.date()))
        p.drawString(x + 400, y - 56, '{}'.format(order.payTime.date()))
        if order.deliveredToAnotherAddress:
            p.drawString(x+2, y-18, 'First name: {}'.format(order.firstNameD))
            p.drawString(x+2,y-36, 'Last name: {}'.format(order.lastNameD))
            p.drawString(x+2,y-54, 'Address: {}'.format(order.addressD))
            p.drawString(x + 2, y - 72, 'City: {}'.format(order.cityD))
            p.drawString(x + 2, y - 90, 'Zip code: {}'.format(order.zipCodeD))
            p.drawString(x + 2, y - 108, 'Telephone number: {}'.format(
                order.telephoneNumberD))
        else:
            p.drawString(x+2, y-18, 'First name: {}'.format(order.user.firstName))
            p.drawString(x + 2, y - 36, 'Last name: {}'.format(order.user.lastName))
            p.drawString(x + 2, y - 54, 'Address: {}'.format(order.user.address))
            p.drawString(x + 2, y - 72, 'City: {}'.format(order.user.city))
            p.drawString(x + 2, y - 90, 'Zip code: {}'.format(order.user.zipCode))
            p.drawString(x + 2, y - 108, 'Telephone number: {}'.format(
                order.user.telephoneNumber))
        p.setFillColorRGB(220,220,220)
        p.line(0, 572, 1000, 572)
        p.setFillColorRGB(0, 0, 0)
        x = 30
        y = 540

        #items
        p.setFont("Helvetica", 15, leading=None)
        p.drawString(x, y, 'Product:')
        p.drawString(x + 120, y, 'Size:')
        p.drawString(x + 240, y, 'Quantity:')
        p.drawString(x + 360, y, 'Cost per item:')
        p.drawString(x + 480, y, 'Cost:')
        p.setFont("Helvetica", 12, leading=None)
        count = 1
        for item in order:
            prodName = str(item.product)
            if len(prodName) > 15:
                prodName = prodName[:12]+'...'
            p.drawString(x, y - count * 22, '{}'.format(prodName))
            p.drawString(x + 120, y - count * 22, '{}'.format(item.size))
            p.drawString(x + 240, y - count * 22, '{}'.format(item.quantity))
            p.drawString(x + 360, y - count * 22, '{}'.format(item.costPerItem))
            p.drawString(x + 480, y - count * 22, '{}'.format(item.productCost))
            count += 1
        p.drawString(x, y - count * 22, 'Shipping:')
        p.drawString(x + 480, y - count * 22, '{}'.format(order.shipCost))
        count += 1
        p.setFont("Helvetica", 15, leading=None)
        p.drawString(x, y - count * 22 - 12, 'Total cost:')
        p.drawString(x + 480, y - count * 22 - 12, '{}'.format(order.orderCost))
        p.drawString(x + 400, 80, 'Online Shop Team')

        p.setTitle('Invoice_{}'.format(OrderId))
        p.showPage()
        p.save()

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

        return response

    else:
        return HttpResponseNotFound('You cannot do it!')
