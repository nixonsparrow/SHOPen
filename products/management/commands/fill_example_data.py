import random
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.translation import gettext

from products.models import Category, Item, Product


class Command(BaseCommand):
    help = "Fill database tables related for products application"
    categories_arg = 10
    items_arg = 100
    orders_arg = 20
    products_arg = 50

    def add_arguments(self, parser):
        parser.add_argument(
            "--categories",
            type=int,
            help=gettext("Specify number of Category objects created, default=")
            + str({self.categories_arg}),
        )
        parser.add_argument(
            "--items",
            type=int,
            help=gettext("Specify number of Item objects created, default=")
            + str({self.items_arg}),
        )
        parser.add_argument(
            "--products",
            type=int,
            help=gettext("Specify number of Product objects created, default=")
            + str({self.products_arg}),
        )

    def handle(self, *args, **options):
        categories_arg = options["categories"] or self.categories_arg
        items_arg = options["items"] or self.items_arg
        products_arg = options["products"] or self.products_arg

        self.stdout.write(
            "Preparing to create: %s categories, %s products and %s items..." % (categories_arg, products_arg, items_arg)
        )

        try:
            # transaction atomic makes that safer - if any error happens, then objects will not be created
            with transaction.atomic():
                categories = Category.objects.bulk_create(
                    (Category(name=f"Category_{i}") for i in range(categories_arg))
                )
                products = Product.objects.bulk_create(
                    (
                        Product(
                            name=f"Product_{i}",
                            category_id=random.choice(categories).id,
                            price=Decimal(random.randrange(10000) / 100),
                            image="default.jpg",
                            thumbnail="default_thumbnail.jpg",
                            quantity=10,
                        )
                        for i in range(products_arg)
                    )
                )

                items = []
                for i in range(items_arg):
                    product = random.choice(products)
                    items.append(
                        Item(product_id=product.id, quantity=1, price=product.price)
                    )

                    # BaseCommand does not initiate signal about quantity, so it's subtracted manually
                    product.quantity -= 1
                    product.save(update_fields=["quantity"])
                    if product.quantity < 1:
                        del products[products.index(product)]
                        if not products:
                            break

                Item.objects.bulk_create(items)

        # if there is any error - finish command with error message
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    "Error occured: %s\nData have not been saved to database." % e
                )
            )
            return

        self.stdout.write(self.style.SUCCESS("Successfully added data."))
