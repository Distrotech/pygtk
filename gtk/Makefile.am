
INCLUDES = -I$(top_srcdir) $(PYTHON_INCLUDES) $(PYTHON_CFLAGS) $(GTK_CFLAGS)

pyexec_LTLIBRARIES = _gtkmodule.la

_gtkmodule_la_LDFLAGS = -module -avoid-version
_gtkmodule_la_SOURCES = \
	pygtk.h \
	pygtk-private.h \
	gtkobject-support.c \
	gtk-types.c

