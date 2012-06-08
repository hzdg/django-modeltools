import os.path
import re
from string import Formatter


class Wrapper(object):
    """Wraps a model to provide access to attributes as dict values so that it
    can be used with formatter classes.

    """
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def __getitem__(self, key):
        return getattr(self._wrapped, key)


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
