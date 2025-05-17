__all__ = ()

from http import HTTPStatus

from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.views import View

from storage.models import File


class DownloadStorageFileView(View):
    def get(self, request, file_path, filename):
        file_path = settings.MEDIA_ROOT / file_path
        if File.owned.catalog(request.user).filter(file__contains=filename).exists():
            return FileResponse(open(file_path, 'rb'), as_attachment=True)

        return HttpResponse(status=HTTPStatus.NOT_FOUND)
