from django.db.models import Manager


class FilteredManager(Manager):
    def __init__(self, **kwargs):
        self.filter_args = kwargs
        super(FilteredManager, self).__init__()

    def get_query_set(self):
        return super(FilteredManager, self).get_query_set() \
                .filter(**self.filter_args)


class CustomQuerySetManager(Manager):
    """
    A manager that uses a custom QuerySet class. If you access a property that
    doesn't exist on the manager, it will attempt to proxy to the queryset. This
    behavior is consistent with methods like ``all()``, ``filter()`` and
    ``exclude()`` which are also available via the manager.

    Example::

        class MyCustomQS(QuerySet):
            def current(self):
                return self.exclude(start_time__gt=now) \
                        .exclude(end_time__lt=now)

        class MyModel(models.Model):
            objects = CustomQuerySetManager(MyCustomQS)

        m = MyModel.objects.get(pk=1)
        m.objects.all().current()  # Access the ``current()`` method of the queryset
        m.objects.current()  # Also works!

    """
    def __init__(self, queryset_class, *args, **kwargs):
        self.queryset_class = queryset_class
        super(CustomQuerySetManager, self).__init__(*args, **kwargs)

    def __getattr__(self, attr):
        qs = self.get_query_set()
        try:
            return getattr(qs, attr)
        except AttributeError:
            raise

    def get_query_set(self):
        return self.queryset_class(self.model, using=self._db)
