from django import template

register = template.Library()

forbidden_words = ['гадкими,', 'гадких', 'мерзкими,', 'отвратительными', 'омерзительными,', 'дурак.']


@register.filter()
def censor(text):
    text1 = text.split()
    for i, word in enumerate(text1):
        if word in forbidden_words:
            text1[i] = word[0] + '***,'
    return ' '.join(text1)





