from django.template.defaulttags import register

@register.filter(name="dict_key")
def get_item(dictionary, key):
    return dictionary.get(key)