from django import template

register = template.Library()


def is_client(user):
    return user.groups.filter(name="Client").exists()


def is_vendor(user):
    return user.groups.filter(name="Vendor").exists()


register.filter("is_client", is_client)
register.filter("is_vendor", is_vendor)
