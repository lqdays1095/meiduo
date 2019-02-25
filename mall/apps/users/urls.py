from django.conf.urls import url
from . import views
urlpatterns =[
    url(r'^usernames/(?P<username>\w{5,20})/$', views.RegisterUsernameCountAPIView.as_view(), name='usernamecount'),
    url(r'^phones/(?P<mobile>1[345789]\d{9})/$', views.RegisterPhoneCountAPIView.as_view()),
    url(r'^users/$', views.RegisterCreateView().as_view())
]