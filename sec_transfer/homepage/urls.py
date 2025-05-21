from django.urls import path

from homepage.views import HomepageIndexView

app_name = 'homepage'

urlpatterns = [
    path('', HomepageIndexView.as_view(), name='index'),
]
