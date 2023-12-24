from django import template


register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.


def censor(value):
   STOP_LIST = [
   'редиска',
   'хрен',
   'блин',
   'писец',
   'писос'
]
   for word in STOP_LIST:
      value = value.replace(word, word[:1]+'*' * (len(word)-1))
   return value


register.filter('censor', censor)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()