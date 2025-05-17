from django.urls import re_path

from download.views import DownloadStorageFileView

app_name = 'download'

urlpatterns = [
    re_path(
        r'media/(?P<file_path>storage/.+/(?P<filename>.+))',
        DownloadStorageFileView.as_view(),
        name='media',
    ),
]
