
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
