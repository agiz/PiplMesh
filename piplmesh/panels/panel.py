import os, pkgutil

from django.utils import importlib

# A fake panel module which loads all bundled panels instead

for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]):
    for file in ('panel', 'models', 'tasks'):
        try:
            importlib.import_module('.%s.%s' % (module, file), 'piplmesh.panels')
        except ImportError, e:
            message = str(e)
            if message != 'No module named %s' % (file,):
                raise
