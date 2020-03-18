from django.utils import timezone
from django.urls import reverse
from django.http import Http404
from django.shortcuts import render, redirect
from django.http import request
from django_countries import countries
from django.views.generic import ListView, DetailView
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


"""
# function based view
def room_detail(request, pk):

    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room": room},)
    except models.Room.DoesNotExist:  # 존재하지 않는 Room id일 경우 예외처리
        # return redirect(reverse("core:home")) # 첫페이지로 리다이렉트
        raise Http404()
"""

# class based view
class RoomDetail(DetailView):
    model = models.Room
    # pk_url_kwarg = ""  : 디폴트는 pk, 때문에 url의 인자를 pk로 설정해두면 알아서 pk값으로 매핑시킴.
    # 예외발생 시 알아서 처리. (404에러)


def search(request):

    city = str.capitalize(request.GET.get("city", "Anywhere"))
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = request.GET.get("instant")
    superhost = request.GET.get("superhost")
    # getlist
    s_amenities = bool(request.GET.getlist("amenities", False))
    s_facilities = bool(request.GET.getlist("facilities", False))
    print(s_amenities)
    form = {  # from Form : url로부터 받은 데이터
        "city": city,
        "s_country": country,
        "s_room_type": room_type,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "instant": instant,
        "superhost": superhost,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {  # from Database
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    return render(request, "rooms/search.html", context={**form, **choices},)
    ##   ** : unpacking

