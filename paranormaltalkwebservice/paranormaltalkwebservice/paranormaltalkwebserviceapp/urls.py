from django.conf.urls import url,include
from django.contrib import admin
from . import views


#from rest_framework.urlpatterns import format_suffix_patterns




urlpatterns = [



    #url(r'^stock/$', views.StockList.as_view(),name="stocklist"),
    url(r'^registeruser/$', views.RegisterUser.as_view(),name="registeruser"),
    #url(r'^updateuser/$', views.UpdateUser.as_view(),name="updateuser"),
    url(r'^login/$', views.Login.as_view(),name="login"),
    url(r'^logout/$', views.Logout.as_view(),name="logout"),
]