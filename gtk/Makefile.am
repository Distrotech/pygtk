
INCLUDES = -I$(top_srcdir) $(PYTHON_INCLUDES) $(GTK_CFLAGS)

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

# chmod hack here is because automake guys decided distdir should be
# read only for the next version :(
$(srcdir)/gtk.c: $(srcdir)/gtk.defs $(srcdir)/gtk.override
	-chmod a+w $(srcdir)
	cd $(srcdir) \
	&& $(PYTHON) ../codegen/codegen.py gtk.defs gtk.override > gen-gtk.c \
	&& cp gen-gtk.c gtk.c \
	&& rm -f gen-gtk.c

# a hack so that gtk.c is not included in the final package.
dist-hook:
	-rm -f $(distdir)/gtk.c

EXTRA_DIST = gtk.defs gtk.override

