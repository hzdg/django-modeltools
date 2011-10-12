import os.path
import re
from string import Formatter
from django.db.models import Manager


class FilenameFormatter(Formatter):
    """
    Formats values for use in a filename.

    """
    def __init__(self, lowercase, nonwordchars, word_delimiter='_'):
        self.lowercase = lowercase
        self.nonwordchars = nonwordchars
        self.word_delimiter = word_delimiter

    def format_field(self, value, format_spec):
        """Formats the fields according to the options provided to the
        constructor.

        """
        value = super(FilenameFormatter, self).format_field(value, format_spec)
        if self.lowercase:
            value = value.lower()
        if not self.nonwordchars:
            value = re.sub('[^\w\s]+', '', value)
        value = re.sub('\s+', self.word_delimiter, value)
        return value


class Wrapper(object):
    """Wraps a model to provide access to attributes as dict values so that it
    can be used with formatter classes.

    """
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def __getitem__(self, key):
        return getattr(self._wrapped, key)


def format_filename(pattern, add_extension=True, lowercase=True, nonwordchars=False, word_delimiter='_'):
    """
    Creates a method to be used as a value for Django models' upload_to
    argument. The returned method will format a filename based on properties of
    the model.
    
    Usage:
        thumbnail = models.ImageField(upload_to=format_filename('profile_images/{last_name}_{first_name}'))
    """
    def upload_to(self, old_filename):
        extension = os.path.splitext(old_filename)[1]
        formatter = FilenameFormatter(lowercase=lowercase,
                nonwordchars=nonwordchars, word_delimiter=word_delimiter)
        filename = formatter.vformat(pattern, [], Wrapper(self))
        if add_extension:
            filename += extension
        return filename

    return upload_to


class Enum(object):
    """
    A class for easily creating enumeration types.
    
    Usage::
    
        # models.py
        class MyModel(models.Model):
            
            Color = Enum(
                RED=('r', 'Red'),
                GREEN=('g', 'Green'),
                BLUE=('b', 'Blue'),
            )

            color = models.CharField(max_length=1, choices=Color.choices())
        
        # Elsewhere...
        m = MyModel.objects.filter(color=MyModel.Color.RED)
    
    """
    
    def __init__(self, *args, **kwargs):
        """
        Accepts kwargs where the keyword is the constant name and the value is
        a tuple containing the ENUM value and a label. If order is important
        (i.e. for choices), you can also pass 3-tuples::

            Color = Enum(
                ('RED', 'r', 'Red'),
                ('GREEN', 'g', 'Green'),
                ('BLUE', 'b', 'Blue'),
            )

        """
        self._constlist = list(args)
        choices = []
        for key, (value, label) in kwargs.items():
            self._constlist.append((key, value, label))
        for key, value, label in self._constlist:
            setattr(self, key, value)
            choices.append((key, label))
        self.__choices = choices

    def choices(self):
        """
        Returns a list formatted for use as field choices.
        (See https://docs.djangoproject.com/en/dev/ref/models/fields/#choices)
        """
        return [(v, l) for k, v, l in self._constlist]

    def keys(self):
        return [k for k, v, l in self._constlist]

    def values(self):
        return [v for k, v, l in self._constlist]

    def labels(self):
        return [l for k, v, l in self._constlist]

    def get_label(self, enum_value):
        for key, value, label in self._constlist:
            if enum_value == value:
                return label


class FilteredManager(Manager):
    def __init__(self, **kwargs):
        self.filter_args = kwargs
        super(FilteredManager, self).__init__()
    def get_query_set(self):
        return super(FilteredManager, self).get_query_set() \
                .filter(**self.filter_args)
