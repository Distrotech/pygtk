
INCLUDES = -I$(top_srcdir) $(PYTHON_INCLUDES) $(PYTHON_CFLAGS) $(GTK_CFLAGS)

pyexec_LTLIBRARIES = _gtkmodule.la

_gtkmodule_la_LDFLAGS = -module -avoid-version
_gtkmodule_la_LIBADD = $(GTK_LIBS)
_gtkmodule_la_SOURCES = \
	pygtk.h \
	pygtk-private.h \
	gtkmodule.c \
	gtkobject-support.c \
	gtk-types.c \
	gtkobjects.c

