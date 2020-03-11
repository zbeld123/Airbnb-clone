from math import ceil
from . import models
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def all_rooms(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()  # all()을 호출해도 쿼리셋을 만들뿐, 즉시 모든 데이터베이스에 접근하진 않음
    paginator = Paginator(room_list, 10)  # Room의 요소를 10개씩 불러오도록 세팅
    rooms = paginator.get_page(page)
    return render(request, "rooms/home.html", context={"rooms": rooms},)

