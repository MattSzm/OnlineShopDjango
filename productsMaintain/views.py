from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from . import models
from .forms import SizeChooseForm
from cart.cart import Cart


class ProductListView(TemplateResponseMixin, View):
    model = models.Product
    template_name = 'products/product/list.html'

    def get(self, request, category_slug=None):
        products = models.Product.objects.all().filter(
                                        available=True)
        categories = models.Category.objects.all()

        category = None
        if category_slug:
            category = get_object_or_404(models.Category,
                                         slug=category_slug)
            products = products.filter(category=category)
        return self.render_to_response({'products': products,
                                        'categories': categories,
                                        'categoryOfProducts': category,
                                        'section': 'products'})


class ProductDetailView(TemplateResponseMixin, View):
    models = models.Product
    template_name = 'products/product/detail.html'

    def get(self, request, category_slug, product_slug, id_image=None):
        product = get_object_or_404(models.Product,
                                    slug=product_slug)
        categories = models.Category.objects.all()
        form = SizeChooseForm()
        form.fields['sizes'].queryset = models.Size.objects.filter(
            ProductWithThisSize__in=[product])

        if id_image:
            main_image = get_object_or_404(models.ImageOfProduct, id=id_image)
        else:
            main_image = product.mainImage

        return self.render_to_response({'product': product,
                                        'form': form,
                                        'section': 'products',
                                        'categories': categories,
                                        'categoryOfProductSlug':
                                        category_slug,
                                        'main_image': main_image})

    def post(self, request, category_slug, product_slug):
        cart = Cart(request)
        product = get_object_or_404(models.Product,
                                    slug=product_slug)
        size = models.Size.objects.get(id=request.POST['sizes'])
        if size:
            cart.addProduct(product, 1, size.id)
            return redirect('cart:cartDetail')
        return redirect(product)



