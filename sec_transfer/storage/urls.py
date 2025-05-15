from django.urls import path

from storage import views

app_name = 'storage'

urlpatterns = [
    path('', views.FileCatalogView.as_view(), name='catalog'),
]
