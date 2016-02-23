from django.conf.urls import url

from apps.home import views


urlpatterns = [
    url(r'^$', views.Home.as_view(), name='index'),
    url(r'^apns/$', views.APNSTester.as_view(), name='apns'),
    url(r'^gcm/$', views.GCMTester.as_view(), name='gcm'),
]
