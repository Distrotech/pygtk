
INCLUDES = -I$(top_srcdir) $(PYTHON_INCLUDES) $(PYTHON_CFLAGS) $(GTK_CFLAGS)

pysitedir = $(PYTHON_SITE)
pysite_PYTHON = __init__.py GTK.py GDK.py

pyexecdir = $(PYTHON_SITE_EXEC)
pyexec_LTLIBRARIES = _gtkmodule.la

_gtkmodule_la_LDFLAGS = -module -avoid-version
_gtkmodule_la_LIBADD = $(GTK_LIBS)
_gtkmodule_la_SOURCES = \
	pygtk.h \
	pygtk-private.h \
	gtkmodule.c \
	gtkobject-support.c \
	gtk-types.c \
	gtk.c

$(srcdir)/gtk.c: gtk.defs gtk.override
	cd $(srcdir) \
	&& $(PYTHON) ../codegen/codegen.py gtk.defs gtk.override > gen-gtk.c \
	&& cp gen-gtk.c gtk.c \
	&& rm -f gen-gtk.c

