import django_filters
from django.forms import DateTimeInput, Textarea
from django_filters import FilterSet, ModelMultipleChoiceFilter, DateTimeFilter
from .models import Item, Category, Reply


class ItemFilter(FilterSet):
    header = django_filters.CharFilter(lookup_expr='icontains', label='Header item')

    category = ModelMultipleChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Category',
        # empty_label='все категории',
        conjoined=False
    )

    time_add = DateTimeFilter(
        field_name='date',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y:%m:%d',
            attrs={'type': 'date'},
        )
    )


class ReplyFilter(FilterSet):
    text = django_filters.CharFilter(lookup_expr='icontains', label='Text')

    items = ModelMultipleChoiceFilter(
        field_name='item',
        queryset=Item.objects.all(),
        label='Items',
        # empty_label='все категории',
        conjoined=False
    )

    date = DateTimeFilter(
        field_name='date',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y:%m:%d',
            attrs={'type': 'date'},
        )
    )

