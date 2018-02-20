# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, InvalidPage
from .models import Category, Good

# Create your views here.


def index(request, cat_id):
    try:
        page_num = request.GET["page"]
    except KeyError:
        page_num = 1

    cats = Category.objects.all()
    if cat_id is None:
        cat = Category.objects.first()
    else:
        try:
            cat = Category.objects.get(pk=cat_id)
        except Category.DoesNotExist:
            raise Http404
    paginator = Paginator(Good.objects.filter(category=cat).order_by("name"), 2)
    try:
        goods = paginator.page(page_num)
    except InvalidPage:
        goods = paginator.page(1)
    return render(request, "index.html", {"category": cat, "cats": cats, "goods": goods})


def categories(request):
    cats = Category.objects.all()
    result = "<br><br>".join(["{}".format(cat.name) for cat in cats])
    return HttpResponse(result)


def good(request, good_id):
    try:
        page_num = request.GET["page"]
    except KeyError:
        page_num = 1
    cats = Category.objects.all()
    try:
        good = Good.objects.get(pk=good_id)
    except Good.DoesNotExist:
        raise Http404
    return render(request, "good.html", {"cats": cats, "good": good, "pn": page_num})
