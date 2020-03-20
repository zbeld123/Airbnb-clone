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

    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    # getlist
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")
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

    filter_args = {}

    if city != "Anywhere":  # city filter
        filter_args["city__startswith"] = city

    filter_args["country__exact"] = country  # country filter

    if room_type != 0:
        filter_args["room_type__pk__exact"] = room_type  # room_type filter

    if price != 0:
        filter_args["price__lte"] = price  # price filter (less then equals)

    if guests != 0:
        filter_args["guests__gte"] = guests  # guests filter (greater then equals)

    if bedrooms != 0:
        filter_args["beedrooms_gte"] = bedrooms  # guests filter (greater then equals)

    if beds != 0:
        filter_args["beds__gte"] = beds  # guests filter (greater then equals)

    if baths != 0:
        filter_args["baths__gte"] = baths  # guests filter (greater then equals)

    if instant is True:
        filter_args["instant_book"] = instant

    if superhost is True:
        filter_args["host__superhost"] = superhost

    # amenities , facilities m-to-m rel filtering
    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)

    rooms = models.Room.objects.filter(**filter_args)

    return render(
        request, "rooms/search.html", context={**form, **choices, "rooms": rooms},
    )
    ##   ** : unpacking

