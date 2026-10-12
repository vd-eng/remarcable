from django import forms

from .models import Category, Tag


class ProductFilter(forms.Form):
    """Search and filter products on the index page."""

    q = forms.CharField(
        required=False,
        label='Search description'
    )

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
