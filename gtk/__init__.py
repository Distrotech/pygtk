# -*- Mode: Python; py-indent-offset: 4 -*-

# hack so that ltihooks is used when importing ExtensionClass ...
import ExtensionClass
del ExtensionClass

# load the required modules:
from GTK import *
import GDK
from _gtk import *

# old names compatibility ...
mainloop = main
def mainquit(*args):
    main_quit()
mainiteration = main_iteration

load_font = font_load
load_fontset = fontset_load

# for importing ...
__all__ = ['_gtk', 'GTK', 'GDK', 'imlib' ]

