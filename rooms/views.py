from math import ceil
from . import models
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

"""
def all_rooms(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()  # all()을 호출해도 쿼리셋을 만들뿐, 즉시 모든 데이터베이스에 접근하진 않음
    # Room의 요소를 10개씩 불러오도록 세팅
    # orphans : page의 마지막 요소가 orphans로 설정한 값보다 같거나 작다면 마지막페이지에 모두 표시
    #           ex) 10개씩 표시하는데 15개의 요소가 있다. orphans=5 ==> 1개 페이지에 모두 표시됨 16개라면 2페이지에 6개 요소 표시
    paginator = Paginator(room_list, 10, orphans=5)
    # page()  <-->  get_page()
    # page : 예외상황 발생시(page index error, page type error ...) 에러 발생시킴 (에러를 컨트롤 할 수 있음)
    # get_page() : 위와 같은 에러 발생시 예외상황 처리 (empty page => 첫번째 페이지로  초과된 페이지번호 요청시 마지막 페이지가 요청되도록 ..)
    rooms = paginator.get_page(page)
    return render(request, "rooms/home.html", context={"page": rooms},)
"""


def all_rooms(request):
    page = request.GET.get("page", 1)  # 디폴트 = 1
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)
    try:
        rooms = paginator.page(int(page))
        return render(request, "rooms/home.html", {"page": rooms},)
    except EmptyPage:
        return redirect("/")

