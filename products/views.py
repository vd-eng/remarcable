from django.views import generic

from .models import Product


class IndexView(generic.ListView):
    template_name = 'products/index.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return Product.objects.all()
