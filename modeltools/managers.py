from django.db.models import Manager


class FilteredManager(Manager):
    def __init__(self, **kwargs):
        self.filter_args = kwargs
        super(FilteredManager, self).__init__()
    def get_query_set(self):
        return super(FilteredManager, self).get_query_set() \
                .filter(**self.filter_args)
