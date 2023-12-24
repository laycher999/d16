from django_filters import FilterSet, CharFilter, DateFromToRangeFilter
from .models import Post
from django_filters.widgets import DateRangeWidget

# Создаем свой набор фильтров для модели Post
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.

from django_filters import FilterSet, CharFilter, DateFilter


from .models import Post


class PostFilter(FilterSet):
    author = CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Автор'
    )
    
    post_time = DateFilter(
        field_name = 'time_in',
        lookup_expr='gt',
        label='От текущей даты'
    )
    
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок'
    )
    class Meta:
        model = Post
        fields = {'title'}


