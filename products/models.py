from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django_advance_thumbnail import AdvanceThumbnailField

from products.utils import get_payment_to_date

User = get_user_model()


class BaseModel(models.Model):
    """Base abstract model to add fields for every other model."""

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(BaseModel):
    """Categories that can be related to Product objects."""

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    name = models.CharField(_("name"), max_length=64, null=False, blank=False)

    def __str__(self):
        return self.name


class Product(BaseModel):
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
    image = models.ImageField(_("image"), upload_to="images/")
    thumbnail = AdvanceThumbnailField(
        source_field="image",
        upload_to="images/thumbnails/",
        size=(200, 200),
        editable=False,
    )
    quantity = models.IntegerField(_("quantity"), default=0)

    def __str__(self):
        return self.name


class Item(BaseModel):
    """Item is an object that puts Product in Cart with wanted quantity.
    Price field is needed because the price can be different from current one."""

    class Meta:
        verbose_name = _("item")
        verbose_name_plural = _("items")

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveSmallIntegerField(_("quantity"), default=0)
    price = models.DecimalField(
        _("price"), max_digits=8, decimal_places=2, null=False, blank=False
    )

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) - {self.price:.2f})"


class Order(BaseModel):
    """Order that User with role Client can place and purchase products by."""

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders", null=False, blank=False
    )
    items = models.ManyToManyField(Item, verbose_name=_("items"), blank=True)
    address = models.CharField(_("address"), max_length=64, null=False, blank=False)
    order_datetime = models.DateTimeField(
        _("order date and time"), default=timezone.now
    )
    payment_to = models.DateField(_("payment to"), default=get_payment_to_date)

    @property
    def price_total(self):
        return self.items.aggregate(Sum("price"))["price__sum"]

    def get_items_string(self):
        items_string = ""
        for item in self.items.all():
            items_string += f"{item.product.__str__()}, "
        return items_string[:-2]

    def send_confirmation_mail(self):
        subject = gettext("Order confirmed")
        message = gettext(
            f"Your order of: {self.get_items_string()} has been confirmed."
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.client.email],
            fail_silently=False,
        )

    def send_remainder_mail(self):
        subject = gettext("Kindly remainder")
        message = gettext(
            f"Your order of: {self.get_items_string()} has not been paid yet."
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.client.email],
            fail_silently=False,
        )
