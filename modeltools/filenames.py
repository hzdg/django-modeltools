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
        wrapped_item = getattr(self._wrapped, key, None)
        if not wrapped_item:
            wrapped_item = getattr(self, key, None)
        if wrapped_item:
            return wrapped_item


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


class MultiFormatter(Formatter):
    def __init__(self, formatter_map, default=None):
        self.formatter_map = formatter_map
        self.default = default

    def get_field(self, field_name, *args, **kwargs):
        if field_name in self.formatter_map:
            formatter = self.formatter_map[field_name]
        else:
            formatter = self.default
        return formatter.get_field(field_name, *args, **kwargs)


def format_filename(pattern, add_extension=True, lowercase=True, nonwordchars=False, word_delimiter='_'):
    """
    Creates a method to be used as a value for Django models' upload_to
    argument. The returned method will format a filename based on properties of
    the model.

    Usage:
        thumbnail = models.ImageField(upload_to=format_filename('profile_images/{last_name}_{first_name}'))
    """
    def upload_to(self, old_filename):
        __filename, __ext = os.path.splitext(
                os.path.basename(old_filename))

        replacers = Wrapper(self)
        replacers.__filename = __filename
        replacers.__ext = __ext

        default_formatter = FilenameFormatter(lowercase=lowercase,
                nonwordchars=nonwordchars, word_delimiter=word_delimiter)
        formatter_map = {
            '__ext': FilenameFormatter(lowercase=lowercase,
                nonwordchars=False, word_delimiter=word_delimiter),
            '__filename': FilenameFormatter(lowercase=lowercase,
                nonwordchars=False, word_delimiter=word_delimiter),
        }

        formatter = MultiFormatter(formatter_map, default=default_formatter)
        filename = formatter.vformat(pattern, [], replacers)

        # For backwards compatibility
        if add_extension and __ext not in filename:
            filename += __ext

        return filename

    return upload_to
