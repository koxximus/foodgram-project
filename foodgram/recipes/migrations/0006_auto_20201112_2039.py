# Generated by Django 3.1.2 on 2020-11-12 20:39

from django.db import migrations
import json


def code(apps, schema_editor):
    Ingredient = apps.get_model("recipes", "Ingredient")
    ingredients = []
    with open("ingredients.json", "r", encoding="utf-8", newline='') as jf:
        data = json.load(jf)
        for row in data:
            ingredients.append(Ingredient(title=row["title"], dimension=row["dimension"]))
    Ingredient.objects.bulk_create(ingredients)


def reverse_code(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20201108_2003'),
    ]

    operations = [
        migrations.RunPython(code, reverse_code=reverse_code),
    ]
