from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from localflavor.us.models import USPostalCodeField
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class ShopUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        if kwargs.get('is_superuser'):
            user.is_staff = True

        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **kwargs):
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_superuser') is False:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **kwargs)


class ShopUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('e-mail'), max_length=50,
                                   unique=True)
    firstName = models.CharField(_('first name'),
                                 max_length=30, blank=True)
    lastName = models.CharField(_('last name'),
                                max_length=30, blank=True)
    address = models.CharField(_('address'),
                               max_length=100, blank=True)
    city = models.CharField(_('city'), max_length=40,
                            blank=True)
    zipCode = USPostalCodeField(_('zip code'), blank=True)

    telephoneNumber = models.CharField(_('telephone number'), max_length=12,
                                       blank=True)
    photo = models.ImageField(_('avatar'), upload_to='users/',
                              blank=True, null=True)

    dataJoined = models.DateTimeField(_('data joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True, blank=True)
    is_staff = models.BooleanField(_('staff'), default=False)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    object = ShopUserManager()

    def get_full_name(self):
        return '{} {}'.format(self.firstName, self.lastName)

    def get_short_name(self):
        return self.firstName
