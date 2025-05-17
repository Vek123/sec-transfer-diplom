from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('storage/', include('storage.urls')),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('download.urls')),
]

if settings.DEBUG:
    urlpatterns = [
        path(
            '__debug__/',
            include('debug_toolbar.urls'),
        ),
        *urlpatterns,
    ]
