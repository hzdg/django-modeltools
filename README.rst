Installation
------------

1. ``pip install django-modeltools``


Included Tools
--------------


Enum
````

The ``Enum`` class lets you quickly define enumeration types for model field
values. It uses `Pep 435`__-style enums, but has some extra model-specific
functionality (like the ability to easily add custom labels).


__ http://www.python.org/dev/peps/pep-0435/


Usage
'''''

In models.py:

.. code-block:: python

	from modeltools import Enum

	class MyModel(models.Model):

	    Color = Enum(
	        RED=('r', 'Red'),
	        GREEN=('g', 'Green'),
	        BLUE=('b', 'Blue'),
	    )

	    color = models.CharField(max_length=1, choices=Color.choices())

Elsewhere:

.. code-block:: python

	m = MyModel.objects.filter(color=MyModel.Color.RED)


Custom Labels
'''''''''''''

By default, labels are title-cased versions of your enum member names (e.g.
"Red" for ``Color.RED``). You can customize this with an inner ``Labels`` class.

.. code-block:: python

	class Color(Enum):
	    RED = 'r'
	    GREEN = 'g'
	    BLUE = 'b'

	    class Labels:
	        RED = 'El color del diablo'


format_filename
```````````````

The ``format_filename`` function provides an easy way to name user media (uploaded files) based on properties of the model that stores them.

Usage
`````

In models.py:

.. code-block:: python

	from modeltools import format_filename as _ff

	class Person(models.Model):
		first_name = models.CharField(max_length=50)
		last_name = models.CharField(max_length=50)
		middle_name = models.CharField(max_length=50)
		avatar = models.ImageField(upload_to=_ff('avatars/{last_name}_{first_name}'))

In the above example, ``{first_name}`` and ``{last_name}`` will be replaced with the corresponding values from the ``Person`` instance. The uploaded file will automatically retain its original extension.

.. code-block:: python

	upload_to=_ff('avatars/{last_name}_{first_name}/{__filename}.thumbnail{__ext}')

``{__filename}`` and ``{__ext}`` allows access to the name and extension the file was uploaded with.

By default, the properties used in the formatting pattern will be converted to lowercase, stripped of non-word characters, and have their spaces replaced with underscores. (This behavior can be changed by providing extra arguments to the ``format_filename`` function.) The rest of the formatting string will be unaffected.
