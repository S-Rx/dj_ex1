from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?:(?P<cat_id>\d+)/)?$', views.index, name='index'),
    url(r'^categories/$', views.categories, name='categories'),
    url(r'^good/(?P<good_id>\d+)/$', views.good, name='good'),
]
