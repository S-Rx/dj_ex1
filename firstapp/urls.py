from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required

from .twviews import GoodListView, GoodDetailView, GoodCreate, GoodUpdate, GoodDelete, CategoryCreate

urlpatterns = [
    # url(r'^(?:(?P<cat_id>\d+)/)?$', views.index, name='index'),
    # url(r'^categories/$', views.categories, name='categories'),
    # url(r'^good/(?P<good_id>\d+)/$', views.good, name='good'),

    url(r'^(?:(?P<cat_id>\d+)/)?$', GoodListView.as_view(), name="index"),
    url(r'^good/(?P<good_id>\d+)/$', GoodDetailView.as_view(), name="good"),

    url(r'^add/$', login_required(CategoryCreate.as_view()), name="category_add"),
    url(r'^(?P<cat_id>\d+)/add/$', permission_required("firstapp.add_good")(GoodCreate.as_view()), name="good_add"),
    url(r'^good/(?P<good_id>\d+)/edit/$', permission_required("firstapp.change_good")(GoodUpdate.as_view()),
        name="good_edit"),
    url(r'^good/(?P<good_id>\d+)/delete/$', permission_required("firstapp.delete_good")(GoodDelete.as_view()),
        name="good_delete"),
]
