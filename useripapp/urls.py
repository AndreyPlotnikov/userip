from django.conf.urls import url

urlpatterns = [
    url(r'^link/$', 'useripapp.views.link', name='link'),
]
