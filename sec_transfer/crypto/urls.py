from django.urls import path

from crypto.views import GetPublicKeyView

app_name = 'crypto'

urlpatterns = [
    path('public-key/', GetPublicKeyView.as_view(), name='get-public-key'),
]
