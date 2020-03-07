from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'tracker'

urlpatterns = [
    url(r'^bm/$'          , views.tracker_bm, name="tracker_bm"),
    url(r'^dashboard/$'   , views.tracker_dashboard, name="tracker_dashboard"),
    url(r'^exercise/$'    , views.tracker_exercise, name="tracker_exercise"),
    url(r'^food/$'        , views.tracker_food, name="tracker_food"),
    url(r'^medication/$'  , views.tracker_medication, name="tracker_medication"),
    url(r'^profile/$'     , views.tracker_profile, name="tracker_profile"),
    url(r'^weight/$'      , views.tracker_weight, name="tracker_weight"),
    path('', views.index  , name='index'),
]
