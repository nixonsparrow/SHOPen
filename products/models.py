from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from PIL import Image

from products.utils import two_weeks_from_now

User = get_user_model()


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
    thumbnail = models.ImageField(
        _("thumbnail"), upload_to="uploads/thumbnails", default="default_thumbnail.jpg"
    )
    quantity = models.IntegerField(_("quantity"), default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # make sure that thumbnail is not bigger than 300x300px
        img = Image.open(self.thumbnail.path)
        width, height = img.size  # get dimensions

        # check which one is smaller
        if height < width:
            # make square by cutting off equal amounts left and right
            left = (width - height) // 2
            right = (width + height) // 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))

        elif width < height:
            # make square by cutting off bottom
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))

        if width > 300 and height > 300:
            img.thumbnail((300, 300))

        img.save(self.thumbnail.path)


class Cart(models.Model):
    """Cart is a temporary object to store current data about Products
    that client want to purchase at the moment.
    It changes finally into Order if finalised."""

    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="carts", null=False, blank=False
    )

    @property
    def price_total(self):
        return self.items.aggregate(Sum("price"))["price__sum"]


class Item(models.Model):
    """Item is an object that puts Product in Cart with wanted quantity.
    Price field is needed because the price can be different from current one."""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveSmallIntegerField(_("quantity"), default=0)
    price = models.DecimalField(
        _("price"), max_digits=8, decimal_places=2, null=False, blank=False
    )

    @property
    def price_total(self):
        return self.price * self.quantity


class Order(models.Model):
    """Order that User with role Client can place and purchase products by."""

    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders", null=False, blank=False
    )
    address = models.CharField(_("address"), max_length=64, null=False, blank=False)
    order_datetime = models.DateTimeField(
        _("order date and time"), default=timezone.now
    )
    payment_to = models.DateField(_("payment to"), default=two_weeks_from_now)
    products = models.JSONField(_("products"), default=dict)
    price_total = models.DecimalField(
        _("price total"),
        max_digits=8,
        decimal_places=2,
        null=False,
        blank=False,
    )
