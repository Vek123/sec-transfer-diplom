__all__ = ()

from django.views.generic import TemplateView


class HomepageIndexView(TemplateView):
    template_name = 'homepage/index.html'
