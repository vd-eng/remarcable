from django.views import generic

from .forms import ProductFilter
from .models import Product


class IndexView(generic.ListView):
    template_name = 'products/index.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        self.product_filter = ProductFilter(self.request.GET or None)

        # NOTE: Check if we need to optimize the query here
        qs = Product.objects

        if not self.product_filter.is_bound:
            return qs.all()

        # Trigger form validation to get `cleaned_data` populated.
        self.product_filter.is_valid()

        data = self.product_filter.cleaned_data
        what = data.get('q')
        categories = data.get('categories')
        category_ids = [category.pk for category in categories]
        tags = data.get('tags') or []
        tag_ids = [tag.pk for tag in tags]

        return (qs
            .search(what)
            .of_categories(category_ids)
            .assigned_tags(tag_ids)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.product_filter
        return context
