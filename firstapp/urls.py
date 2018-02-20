from django.conf.urls import url
from . import views
from .twviews import GoodListView, GoodDetailView, GoodCreate, GoodUpdate, GoodDelete

urlpatterns = [
	# url(r'^(?:(?P<cat_id>\d+)/)?$', views.index, name='index'),
	# url(r'^categories/$', views.categories, name='categories'),
	# url(r'^good/(?P<good_id>\d+)/$', views.good, name='good'),

	url(r'^(?:(?P<cat_id>\d+)/)?$', GoodListView.as_view(), name="index"),
	url(r'^good/(?P<good_id>\d+)/$', GoodDetailView.as_view(), name="good"),

	url(r'^(?P<cat_id>\d+)/add/$', GoodCreate.as_view(), name="good_add"),
	url(r'^good/(?P<good_id>\d+)/edit/$', GoodUpdate.as_view(), name="good_edit"),
	url(r'^good/(?P<good_id>\d+)/delete/$', GoodDelete.as_view(), name="good_delete"),
]
