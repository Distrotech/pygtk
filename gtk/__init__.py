# -*- Mode: Python; py-indent-offset: 4 -*-

# hack so that ltihooks is used when importing ExtensionClass ...
import ExtensionClass
del ExtensionClass

# load the required modules:
from GTK import *
import GDK
from _gtk import *

# for importing ...
__all__ = ['_gtk', 'GTK', 'GDK' ]

