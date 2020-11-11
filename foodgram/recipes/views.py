from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import FileResponse
from django.contrib.auth.decorators import login_required


from .models import Tag, Recipe, User
from .forms import RecipeForm
from .functions import check_ingredients, create_ingredient_amount, pdf_create


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)


def index(request):
    tags = request.GET.get("tags", "bld")
    recipes_list = Recipe.objects.filter(tags__value__in=tags).\
        order_by("-pub_date")

    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page, "paginator": paginator, "tags": tags})


@login_required
def my_favorites(request, username):
    profile = get_object_or_404(User, username=username)
    tags = request.GET.get("tags", "bld")
    if not tags:
        recipes_list = Recipe.objects.filter(favorites__follower=profile).\
            order_by("-pub_date")
    else:
        recipes_list = Recipe.objects.filter(favorites__follower=profile).\
            filter(tags__value__in=tags).\
            order_by("-pub_date")

    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page, "paginator": paginator, "tags": tags, "my_favorites": True})


@login_required
def new_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        ingredients = check_ingredients(request)

        if not form.is_valid():
            return render(request, "recipes/recipe.html", {"form": form})
        if not ingredients:
            form.add_error(None, "Это поле пустое или заполненно неправильно.")
            return render(request, "recipes/recipe.html", {"form": form})

        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        recipe.tags.set(Tag.objects.filter(id__in=form.cleaned_data["tags"]))

        create_ingredient_amount(ingredients, recipe)

        return redirect('index')

    form = RecipeForm()
    return render(request, "recipes/recipe.html", {"form": form})


@login_required
def recipe_edit(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, id=recipe_id, author=author)

    if recipe.author != request.user:
        return redirect("recipe_page", recipe_id=recipe_id)

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)

        if not form.is_valid():
            return render(request, "recipes/recipe.html", {"form": form})

        form.save()

        recipe.ingredient_amount.filter(recipe=recipe).delete()
        create_ingredientamount(request, recipe)

        return redirect("recipe_page", username=author.username, recipe_id=recipe_id)

    form = RecipeForm(instance=recipe)
    return render(request, "recipes/recipe.html", {"form": form, "recipe": recipe})


@login_required
def recipe_del(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, id=recipe_id, author=author)

    if recipe.author != request.user:
        return redirect("recipe_page", recipe_id=recipe_id)

    recipe.delete()
    return redirect("author_page", username)


def recipe_page(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    return render(request, "recipes/recipe_page.html", {"recipe": recipe})


def author_page(request, username):
    author = get_object_or_404(User, username=username)
    tags = request.GET.get("tags")
    if not tags:
        recipes_list = author.author_recipes.all().order_by("-pub_date")
    else:
        recipes_list = author.author_recipes.filter(tags__value__contains=tags).order_by("-pub_date")

    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page, "paginator": paginator, "tags": tags, "author": author})


@login_required
def follow_page(request, username):
    profile = get_object_or_404(User, username=username)

    if not profile == request.user:
        return redirect("my_follow", request.user.username)

    follow_list = profile.follower.all().order_by("-following__author_recipes__pub_date")

    paginator = Paginator(follow_list, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "recipes/follow_page.html", {"page": page, "paginator": paginator})


@login_required
def shoplist(request, username):
    customer = get_object_or_404(User, username=username)
    if not customer == request.user:
        return redirect("shoplist", request.user.username)

    purchases = customer.purchases.all()

    return render(request, "recipes/shoplist.html", {"purchases": purchases})


@login_required
def download_shoplist(request, username):
    recipes = Recipe.objects.filter(purchases__customer=request.user).\
        values("ingredients__title", "ingredients__dimension").\
        annotate(amount=Sum("ingredient_amount__amount")).\
        order_by("ingredients__title")

    buffer = pdf_create(recipes)
    return FileResponse(buffer, as_attachment=True, filename='shoplist.pdf')
