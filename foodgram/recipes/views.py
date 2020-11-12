from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .functions import (
    check_ingredients,
    create_ingredient_amount,
    get_tags_and_recipes_list,
    pdf_create,
)
from .models import Recipe, Tag, User


def index(request):
    meals, recipes_list = get_tags_and_recipes_list(request)

    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request,
        "index.html",
        {"page": page, "paginator": paginator, "tags": meals},
    )


@login_required
def my_favorites(request, username):
    profile = get_object_or_404(User, username=username)
    meals, recipes_list = get_tags_and_recipes_list(request)
    recipes_list = recipes_list.filter(favorites__follower=profile)

    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request,
        "index.html",
        {
            "page": page,
            "paginator": paginator,
            "tags": meals,
            "my_favorites": True,
        },
    )


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        ingredients = check_ingredients(request)
        if not ingredients:
            form.add_error(None, "Это поле пустое или заполненно неправильно.")
            return render(request, "recipes/recipe.html", {"form": form})
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        recipe.tags.set(Tag.objects.filter(id__in=form.cleaned_data["tags"]))

        create_ingredient_amount(ingredients, recipe)

        return redirect("index")
    return render(request, "recipes/recipe.html", {"form": form})


@login_required
def recipe_edit(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author__username=username)

    if recipe.author != request.user:
        return redirect("recipe_page", recipe_id=recipe_id)

    form = RecipeForm(
        request.POST or None, request.FILES or None, instance=recipe
    )
    if form.is_valid():
        ingredients = check_ingredients(request)
        if not ingredients:
            form.add_error(None, "Это поле пустое или заполненно неправильно.")
            return render(
                request,
                "recipes/recipe.html",
                {"form": form, "recipe": recipe},
            )

        form.save()

        recipe.ingredient_amounts.filter(recipe=recipe).delete()
        create_ingredient_amount(ingredients, recipe)

        return redirect("recipe_page", username=username, recipe_id=recipe_id)
    return render(
        request, "recipes/recipe.html", {"form": form, "recipe": recipe}
    )


@login_required
def recipe_del(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author__username=username)

    if recipe.author != request.user:
        return redirect("recipe_page", recipe_id=recipe_id)

    recipe.delete()
    return redirect("author_page", username)


def recipe_page(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    return render(request, "recipes/recipe_page.html", {"recipe": recipe})


def author_page(request, username):
    author = get_object_or_404(User, username=username)
    meals, recipes_list = get_tags_and_recipes_list(request)
    recipes_list = recipes_list.filter(author=author)

    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request,
        "index.html",
        {
            "page": page,
            "paginator": paginator,
            "tags": meals,
            "author": author,
        },
    )


@login_required
def follow_page(request, username):
    profile = get_object_or_404(User, username=username)

    if not profile == request.user:
        return redirect("my_follow", request.user.username)

    follow_list = (
        profile.follower.select_related("following")
        .all()
        .order_by("-following__recipes__pub_date")
    )

    paginator = Paginator(follow_list, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request,
        "recipes/follow_page.html",
        {"page": page, "paginator": paginator},
    )


@login_required
def shoplist(request, username):
    customer = get_object_or_404(User, username=username)
    if not customer == request.user:
        return redirect("shoplist", request.user.username)

    purchases = customer.purchases.all()

    return render(request, "recipes/shoplist.html", {"purchases": purchases})


@login_required
def download_shoplist(request, username):
    recipes = (
        Recipe.objects.prefetch_related("ingredients", "ingredient_amounts")
        .filter(purchases__customer=request.user)
        .values("ingredients__title", "ingredients__dimension")
        .annotate(amount=Sum("ingredient_amounts__amount"))
        .order_by("ingredients__title")
    )
    buffer = pdf_create(recipes)
    return FileResponse(buffer, as_attachment=True, filename="shoplist.pdf")
