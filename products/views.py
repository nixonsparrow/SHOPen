from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, TemplateView

from products.forms import OrderForm, UserRegisterForm
from products.models import Item, Order, Product


class HomePage(TemplateView):
    template_name = "products/homepage.html"


class OrderCreateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView
):
    model = Order
    form_class = OrderForm
    extra_context = {
        "extra_title": _("Add Order"),
        "products": Product.objects.filter(quantity__gt=0),
    }
    success_message = _("Order has been successfully added to the database.")
    success_url = reverse_lazy("homepage")

    def test_func(self):
        return self.request.user.groups.filter(name="Client").exists()

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        items_to_create = (
            {"id": int(p[0].replace("product_", "")), "quantity": int(p[1])}
            for p in request.POST.items()
            if "product_" in p[0] and int(p[1]) > 0
        )
        with transaction.atomic():
            items = []
            for item in items_to_create:
                product = Product.objects.get(id=item["id"])
                items.append(
                    Item.objects.create(
                        product_id=product.id,
                        price=product.price,
                        quantity=item["quantity"],
                    )
                )

        return super().post(request, *args, **kwargs)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request,
                gettext("Ac account for %s has been created! You can now log in.")
                % username,
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "registration/register.html", {"form": form})
