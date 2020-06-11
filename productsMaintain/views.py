from django.shortcuts import  get_object_or_404, redirect, render
from django.views.generic.base import TemplateResponseMixin, View
from . import models
from .forms import SizeChooseForm, searchingForm
from cart.cart import Cart
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib import messages
from accounts.recommendationSystem import RecommendationEngine


class ProductListView(TemplateResponseMixin, View):
    model = models.Product
    template_name = 'products/product/list.html'

    def get(self, request, category_slug=None):
        products = models.Product.objects.all().filter(
                                        available=True)
        categories = models.Category.objects.all()
        searchForm = searchingForm()

        category = None
        if category_slug:
            category = get_object_or_404(models.Category,
                                         slug=category_slug)
            products = products.filter(category=category)
        return self.render_to_response({'products': products,
                                        'categories': categories,
                                        'categoryOfProducts': category,
                                        'section': 'products',
                                        'searchForm': searchForm})


class ProductDetailView(TemplateResponseMixin, View):
    models = models.Product
    template_name = 'products/product/detail.html'

    def get(self, request, category_slug, product_slug, id_image=None):
        product = get_object_or_404(models.Product,
                                    slug=product_slug)
        recommendation = RecommendationEngine(request)
        recommendation.addSignle(product.id)

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
            messages.success(request, '{} ({}) successfully added to your cart.'.format(
                product.name, size))
            return redirect('cart:cartDetail')
        return redirect(product)


class BrandListView(TemplateResponseMixin, View):
    model = models.Product
    template_name = 'products/product/listBrand.html'

    def get(self, request, brand_slug, category_slug=None,):
        products = models.Product.objects.all().filter(
                                        available=True)
        brand = get_object_or_404(models.Brand, slug=brand_slug)
        products = products.filter(brand=brand)
        searchForm = searchingForm()

        categories = models.Category.objects.all()
        category = None
        if category_slug:
            category = get_object_or_404(models.Category,
                                         slug=category_slug)
            products = products.filter(category=category)

        return self.render_to_response({'products': products,
                                        'categories': categories,
                                        'categoryOfProducts': category,
                                        'brand': brand,
                                        'section': 'products',
                                        'searchForm': searchForm})

def Searching(request):
    if request.method == 'GET':
        form = searchingForm(request.GET)
        if form.is_valid():
            input = form.cleaned_data['input']

            outputBrand = models.Brand.objects.filter(name__search=input)
            if outputBrand:
                outputBrand = outputBrand[0]
                output = models.Product.objects.filter(
                brand__name__search=outputBrand)

            else:
                searchVector = SearchVector('name', 'description')
                searchQuery = SearchQuery(input)
                searchRank = SearchRank(searchVector, searchQuery)

                output = models.Product.objects.annotate(
                    search=searchVector,
                    rank=searchRank
                ).filter(search=searchQuery).order_by('-rank')

            if output or outputBrand:
                messages.info(request, 'Search results for phrases: {}'.format(
                    input))
                return render(request, 'products/product/searchResults.html',
                              {'output': output,
                               'outputBrand': outputBrand})
    messages.error(request, 'There are no results. ')
    return redirect('product_list')

def MainPange(request):
    Recommendation = RecommendationEngine(request)
    return render(request, 'main/mainPage.html',
                  {'recommendation': Recommendation})
