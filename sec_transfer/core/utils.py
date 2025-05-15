__all__ = ()

from django.db.models import Field


def safe_order_by(queryset, field_name, default_ordering=None):
    model = queryset.model
    clean_field = field_name.lstrip('-')

    if not hasattr(model, clean_field):
        return (
            queryset.order_by(*default_ordering)
            if default_ordering
            else queryset
        )

    field = getattr(model, clean_field).field
    if not isinstance(field, Field):
        return (
            queryset.order_by(*default_ordering)
            if default_ordering
            else queryset
        )

    return queryset.order_by(field_name)
