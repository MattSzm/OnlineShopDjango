from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from . import models

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



