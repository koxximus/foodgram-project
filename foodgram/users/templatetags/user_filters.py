from django import template

from api.models import Favorite, Follow, Purchase

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def has_favor(recipe, user):
    return Favorite.objects.filter(recipe=recipe, follower=user).exists()


@register.filter
def has_follower(author, user):
    return Follow.objects.filter(following=author, follower=user).exists()


@register.filter
def has_customer(recipe, user):
    return Purchase.objects.filter(recipe=recipe, customer=user).exists()
