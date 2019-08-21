from django.conf.urls import url
from . import views

app_name = 'boards'
urlpatterns = [
    url(r'(?P<pk>\d+)/$',views.board_topics,name='board_topics'),
]

