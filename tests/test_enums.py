from modeltools.enums import Enum


def test_choices():
    class Color(Enum):
        __order__ = 'RED GREEN BLUE'

        RED = 'r'
        GREEN = 'g'
        BLUE = 'b'

    COLOR_CHOICES = (
        ('r', 'Red'),
        ('g', 'Green'),
        ('b', 'Blue'),
    )
    assert Color.choices() == COLOR_CHOICES


def test_labels():
    class Color(Enum):
        RED = 'r'
        GREEN = 'g'

        class Labels:
            RED = 'A custom label'

    assert Color.RED.label == 'A custom label'
    assert Color.GREEN.label == 'Green'


def test_query_values():
    """
    Make sure the values that the Django ORM will use in its queries are
    correct.
    """
    class Color(Enum):
        RED = 'r'

    assert Color.RED() == 'r'
