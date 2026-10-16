from django.views import generic

from .forms import ProductFilter
from .models import Product


class IndexView(generic.ListView):
    template_name = 'products/index.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        self.product_filter = ProductFilter(self.request.GET or None)

        # Some of the possible optimizations options is:
        #
        # ```
        # qs = (Product.objects
        #     .select_related('category')
        #     .prefetch_related('tags')
        # )
        # ```
        #
        # What it does is it fetches data for both the primary and the related
        # one-to-many models for `select_related`. For `prefetch_related`,
        # it executes a separate database lookup for each specified relationship and
        # joins the results in Python memory.
        # I don't use that, because the related data (category, tags) is already "straighten"
        # in the queryset via annotations.
        #
        qs = (Product.objects
            .add_category_name()
            .add_tags_as_str()
        )

        if not self.product_filter.is_bound:
            return qs.all()

        # Trigger form validation to get `cleaned_data` populated.
        self.product_filter.is_valid()

        data = self.product_filter.cleaned_data
        what = data.get('q')
        categories = data.get('categories') or []
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
