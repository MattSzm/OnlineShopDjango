from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class Category(models.Model):
    title = models.CharField(_('Title'), max_length=35)
    slug = models.SlugField(max_length=200, db_index=True,
                            unique=True)
    @property
    def numberOfBrands(self):
        return self.brandsOfTheCategory.count()

    @property
    def numberOfProducts(self):
        counter = 0
        for single in self.brandsOfTheCategory.all():
            if single.numberOfProducts > 0:
                counter += single.numberOfProducts
        return counter

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def get_absolute_url(self):
        return reverse('product_list_for_category', args=[self.slug])

class Brand(models.Model):
    category = models.ManyToManyField(Category,blank=True,
                                      related_name='brandsOfTheCategory',)
    """category = models.ForeignKey(Category,
                                related_name='brandsOfTheCategory',
                                    on_delete=models.CASCADE)"""
    name = models.CharField(_('Name'), max_length=35)
    description = models.TextField(_('Description'), blank=True)
    slug = models.SlugField(max_length=200, db_index=True,
                            unique=True)
    logo = models.ImageField(_('Logo'), upload_to='brands/',
                             blank=True, null=True)

    @property
    def numberOfProducts(self):
        return self.products.count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    def get_absolute_url(self):
        pass
        #TODO: implement later


class Size(models.Model):
    size = models.CharField(_('Size'), max_length=5, blank=False)
    value = models.IntegerField(_('Value'))

    def __str__(self):
        return str(self.size).lower()

    class Meta:
        ordering = ('value',)
        verbose_name = _('Size')
        verbose_name_plural = _('Sizes')


class Product(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    description = models.TextField(_('Description'), blank=True)
    slug = models.SlugField(max_length=200, db_index=True,
                            unique=True)

    brand = models.ForeignKey(Brand, related_name='products',
                              on_delete=models.CASCADE)
    category = models.ForeignKey(Category,
                                 related_name='productsOfTheCategory',
                                 on_delete=models.CASCADE,
                                 default=0)

    available = models.BooleanField(_('Available'),
                                    blank=False, default=True)
    isOnSale = models.BooleanField(_('On sale'),
                                   blank=False, default=False)
    price = models.DecimalField(_('Price'),
                                max_digits=8, decimal_places=2)
    priceOnSale = models.DecimalField(_('Price on sale'),
                                max_digits=8, decimal_places=2,
                                      blank=True)

    sizes = models.ManyToManyField(Size, blank=True,
                                   related_name='ProductWithThisSize')
    @property
    def numberOFImages(self):
        return self.images.count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name','price')
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    @property
    def mainImage(self):
        return self.images.all()[0]

    def get_absolute_url(self):
        return reverse('product_detail_view',
                       args=[self.category.slug,
                             self.slug])

class ImageOfProduct(models.Model):
    image = models.ImageField(_('Image'), upload_to='products_images/',
                             blank=True, null=True)
    title = models.CharField(_('Title of Image'), max_length=50,
                             blank=True)
    #title is not obligatory
    product = models.ForeignKey(Product, related_name='images',
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.image.url
