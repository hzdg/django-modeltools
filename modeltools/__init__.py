# Some of the modules (filenames) are not compatible with Python 2.5, but we
# don't want to prevent you from using all of them because of it.

import_errors = []

try:
    from enums import *
except ImportError:
    import_errors.append('enums')

try:
    from filenames import *
except ImportError:
    import_errors.append('filenames')

try:
    from managers import *
except ImportError:
    import_errors.append('managers')

if import_errors:
    import logging
    logger = logging.getLogger('modeltools')
    logger.warning('There were errors importing the following modeltools'
         ' modules: %s. They will not be available. To see the errors, import'
         ' the modules directly.')
