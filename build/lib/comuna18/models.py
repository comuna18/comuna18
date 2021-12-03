import uuid

from django.db import models, IntegrityError
from .utils import generate_random_slug
from django.conf import settings


class ActiveManager(models.Manager):
    def active_objects(self):
        return super().get_queryset().filter(is_active=True)

    def inactive_objects(self):
        return super().get_queryset().filter(is_active=False)



class BaseModel(models.Model):

    PREFIX = ''
    IDENTIFIER_TYPE = 'ID'
    calculated_fields = []

    identifier = models.SlugField(editable=False)

    def get_identifier(self):
        return '{prefix}{id:07}'.format(prefix=self.PREFIX, id=self.id)

    def __str__(self):
        valid_str_names = ('name', 'identifier')
        for valid_str in valid_str_names:
            if getattr(self, valid_str, None):
                return getattr(self, valid_str)
        return super().__str__()

    def get_meta(self):
        return self._meta

    class Meta:
        abstract = True

    def is_protected(self):
        for rel in self._meta.related_objects:
            if rel.on_delete == models.PROTECT:
                if rel.related_name:
                    objects = getattr(self, rel.related_name)
                else:
                    objects = getattr(self, rel.field.model.__name__.lower() + '_set')
                if objects.all():
                    return True
        return False

    def hard_delete(self):
        for rel in self._meta.related_objects:
            if rel.on_delete == models.PROTECT:
                if rel.related_name:
                    objects = getattr(self, rel.related_name)
                else:
                    objects = getattr(self, rel.field.model.__name__.lower() + '_set')
                if objects:
                    try:
                        objects.all().delete()
                    except Exception as e:
                        for obj in objects.all():
                            obj.hard_delete()
        super(BaseModel, self).delete()

    def set_calculated_fields(self):
        for field_name in self.calculated_fields:
            setattr(self, field_name, getattr(self, 'get_' + field_name)())

    def save(self, *args, **kwargs):
        self.identifier = self.get_identifier()
        self.set_calculated_fields()
        super().save(*args, **kwargs)

class RandomSlugModel(BaseModel):

    IDENTIFIER_TYPE = 'SLUG'
    SLUG_LENGTH = getattr(settings, 'SLUG_LENGTH', 6)
    SLUG_IS_PRIMARY_KEY = getattr(settings, 'SLUG_IS_PRIMARY_KEY', False)
    SLUG_IS_NULL = getattr(settings, 'SLUG_IS_NULL', False)

    random_slug = models.SlugField(editable=False, unique=True, primary_key=SLUG_IS_PRIMARY_KEY, null=SLUG_IS_NULL)

    def get_identifier(self):
        return '{prefix}{slug}'.format(prefix=self.PREFIX, slug=self.random_slug)

    def save(self, *args, **kwargs):
        if not self.random_slug:
            self.random_slug = generate_random_slug(model=self._meta.model,
                                                    size=self.SLUG_LENGTH)
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True

class ActiveModel(models.Model):
    ACTIVE_FIELD = 'Activo'
    is_active = models.BooleanField(ACTIVE_FIELD, default=True)
    
    objects = ActiveManager()
    class Meta:
        abstract = True

class TimestampModel(models.Model):

    create_timestamp = models.DateTimeField('Timestamp de creación', auto_now_add=True, editable=False)
    update_timestamp = models.DateTimeField('Timestamp de modificación', auto_now=True, editable=False)

    class Meta:
        abstract = True


