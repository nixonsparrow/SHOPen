from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Categories that can be related to Product objects."""

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    name = models.CharField(_("name"), max_length=64, null=False, blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Products that Clients are able to purchase in SHOPen."""

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    name = models.CharField(_("name"), max_length=64, null=False, blank=False)
    description = models.TextField(
        _("description"), max_length=2048, null=False, blank=False
    )
    price = models.DecimalField(
        _("price"), max_digits=6, decimal_places=2, null=False, blank=False
    )
    category = models.ForeignKey(
        "products.Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    image = models.ImageField(_("image"), upload_to="uploads/", default="default.jpg")
