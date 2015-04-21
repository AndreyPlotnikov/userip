from django.conf.urls import include, url
from django.contrib import admin
import useripapp.urls

urlpatterns = [
    url(r'^userip/', include(useripapp.urls)),
#    url(r'^admin/', include(admin.site.urls)),
]
