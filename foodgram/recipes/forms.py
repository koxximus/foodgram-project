from django import forms
from django.forms import ClearableFileInput

from .models import Recipe, Tag


class MyClearableFileInput(ClearableFileInput):
    def clear_checkbox_name(self, name):
        return name[0]


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=True, widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Recipe
        exclude = ["author", "pub_date", "ingredients"]
        widgets = {
            "description": forms.Textarea(attrs={"row": 8}),
            "time": forms.TextInput(),
            "image": MyClearableFileInput(),
        }
        labels = {
            "title": "Название рецепта",
            "time": "Время приготовления",
            "description": "Описание",
            "image": "Загрузить фото",
        }
