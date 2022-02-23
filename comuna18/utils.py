import string
import random

from django.urls import reverse_lazy, reverse


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    random_chain = ''.join(random.choice(chars) for _ in range(size))
    return random_chain


def generate_random_slug(model, size):
    while True:
        random_slug = id_generator(size=size)
        others = model.objects.filter(random_slug=random_slug)
        if others.count() == 0:
            return random_slug
        break


def picky_reverse(path, kwargs_list=[]):
    while True:
        try:
            kwargs = dict(kwargs_list)
            return reverse(path, kwargs=kwargs)
        except Exception as e:
            kwargs_list = kwargs_list[:-1]
