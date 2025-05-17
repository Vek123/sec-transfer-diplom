from django.urls import path

from storage import views

app_name = 'storage'

urlpatterns = [
    path('', views.FileCatalogView.as_view(), name='catalog'),
    path('create/', views.FileCreateView.as_view(), name='create'),
    path('<int:pk>/delete/', views.FileDeleteView.as_view(), name='delete'),
    path('<int:pk>/update/', views.FileUpdateView.as_view(), name='update'),
]
