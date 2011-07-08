import os.path
import re


class PropertyFormatter(object):
    """
    An object that lazily formats properties of a model, exposing them as
    dictionary keys.
    """
    def __init__(self, model, lowercase, nonwordchars, word_delimiter='_'):
        self.__model = model
        self.__lowercase = lowercase
        self.__nonwordchars = nonwordchars
        self.__word_delimiter = word_delimiter

    def __getitem__(self, key):
        value = str(getattr(self.__model, key))
        if self.__lowercase:
            value = value.lower()
        if not self.__nonwordchars:
            value = re.sub('[^\w\s]+', '', value)
        return re.sub('\s+', self.__word_delimiter, value)

    def keys(self):
        return self.__model.__dict__.keys()


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
        wrapper = PropertyFormatter(self, lowercase=lowercase, nonwordchars=nonwordchars, word_delimiter=word_delimiter)
        filename = pattern.format(**wrapper)
        if add_extension:
            filename += extension
        return filename

    return upload_to


class Enum(object):
    """
    A class for easily creating enumeration types.
    
    Usage:
    
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
    
    def __init__(self, **kwargs):
        """
        Accepts kwargs where the keyword is the constant name and the value is
        a tuple containing the ENUM value and a label
        """
        self.__kwargs = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value[0])
        self.__choices = kwargs.values()

    def choices(self):
        """
        Returns a list formatted for use as field choices.
        (See https://docs.djangoproject.com/en/dev/ref/models/fields/#choices)
        """
        return self.__choices

    def keys(self):
        return self.__kwargs.keys()

    def values(self):
        return [val[0] for val in self.__kwargs.values()]

    def labels(self):
        return [val[1] for val in self.__kwargs.values()]

    def get_label(self, enum_value):
        for key, value in self.__choices:
            if enum_value == key:
                return value