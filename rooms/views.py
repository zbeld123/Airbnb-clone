from django.utils import timezone
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage
from . import models


class SafePaginator(Paginator):
    def validate_number(self, number):
        try:
            return super(SafePaginator, self).validate_number(number)
        except EmptyPage:
            if number > 1:
                return self.num_pages
            else:
                raise


class HomeView(ListView):

    """ Definition HomeView (Class Based View) """

    model = models.Room
    paginator_class = SafePaginator
    paginate_by = 10
    paginate_orphans = 5
    allow_empty = False
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context
