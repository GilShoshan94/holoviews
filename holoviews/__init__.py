
from __future__ import print_function, absolute_import
import os, pydoc

import numpy as np # noqa (API import)
import param


__version__ = str(param.version.Version(fpath=__file__, archive_commit="$Format:%h$",
                                        reponame="holoviews"))

from .core import archive, config                        # noqa (API import)
from .core.dimension import OrderedDict, Dimension       # noqa (API import)
from .core.boundingregion import BoundingBox             # noqa (API import)
from .core.options import (Options, Store, Cycle,        # noqa (API import)
                           Palette, StoreOptions)
from .core.layout import *                               # noqa (API import)
from .core.element import *                              # noqa (API import)
from .core.overlay import *                              # noqa (API import)
from .core.tree import *                                 # noqa (API import)
from .core.spaces import (HoloMap, Callable, DynamicMap, # noqa (API import)
                          GridSpace, GridMatrix)

from .operation import Operation                         # noqa (API import)
from .operation import ElementOperation                  # noqa (Deprecated API import)
from .element import *                                   # noqa (API import)
from .element import __all__ as elements_list
from . import util # noqa (API import)
from .util import extension, renderer, output, opts # noqa (API import)

# Suppress warnings generated by NumPy in matplotlib
# Expected to be fixed in next matplotlib release
import warnings
warnings.filterwarnings("ignore",
                        message="elementwise comparison failed; returning scalar instead")

try:
    import IPython                 # noqa (API import)
    from .ipython import notebook_extension
    extension = notebook_extension # noqa (name remapping)
except ImportError:
    class notebook_extension(param.ParameterizedFunction):
        def __call__(self, *args, **opts): # noqa (dummy signature)
            raise Exception("IPython notebook not available: use hv.extension instead.")

# A single holoviews.rc file may be executed if found.
for rcfile in [os.environ.get("HOLOVIEWSRC", ''),
               os.path.abspath(os.path.join(os.path.split(__file__)[0],
                                            '..', 'holoviews.rc')),
               "~/.holoviews.rc",
               "~/.config/holoviews/holoviews.rc"]:
    filename = os.path.expanduser(rcfile)
    if os.path.isfile(filename):
        with open(filename) as f:
            code = compile(f.read(), filename, 'exec')
            try:
                exec(code)
            except Exception as e:
                print("Warning: Could not load %r [%r]" % (filename, str(e)))
        break

def help(obj, visualization=True, ansi=True, backend=None,
         recursive=False, pattern=None):
    """
    Extended version of the built-in help that supports parameterized
    functions and objects. A pattern (regular expression) may be used to
    filter the output and if recursive is set to True, documentation for
    the supplied object is shown. Note that the recursive option will
    only work with an object instance and not a class.

    If ansi is set to False, all ANSI color
    codes are stripped out.
    """
    backend = backend if backend else Store.current_backend
    info = Store.info(obj, ansi=ansi, backend=backend, visualization=visualization,
                      recursive=recursive, pattern=pattern, elements=elements_list)

    msg = ("\nTo view the visualization options applicable to this "
           "object or class, use:\n\n"
           "   holoviews.help(obj, visualization=True)\n\n")
    if info:
        print((msg if visualization is False else '') + info)
    else:
        pydoc.help(obj)
