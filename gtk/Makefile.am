
INCLUDES = -I$(top_srcdir) $(PYTHON_INCLUDES) $(GTK_CFLAGS) $(GDK_IMLIB_CFLAGS)

if BUILD_IMLIB
imlibmodule = imlibmodule.la
endif
if BUILD_LIBGLADE
libglademodule = libglademodule.la
endif

pysitedir = $(PYTHON_SITE)
pysite_PYTHON = __init__.py GTK.py GDK.py

pyexecdir = $(PYTHON_SITE_EXEC)
pyexec_LTLIBRARIES = _gtkmodule.la $(imlibmodule) $(libglademodule)

_gtkmodule_la_LDFLAGS = -module -avoid-version
_gtkmodule_la_LIBADD = $(GTK_LIBS)
_gtkmodule_la_SOURCES = \
	pygtk.h \
	pygtk-private.h \
	gtkmodule.c \
	gtkobject-support.c \
	gtk-types.c \
	gtk.c

imlibmodule_la_LDFLAGS = -module -avoid-version
imlibmodule_la_LIBADD = $(GDK_IMLIB_LIBS)
imlibmodule_la_SOURCES = \
	pygdkimlib.h \
	imlibmodule.c

libglademodule_la_LDFLAGS = -module -avoid-version
libglademodule_la_LIBADD = $(LIBGLADE_LIBS)
libglademodule_la_SOURCES = \
	libglademodule.c \
	libglade.c

# chmod hack here is because automake guys decided distdir should be
# read only for the next version :(
$(srcdir)/gtk.c: $(srcdir)/gtk.defs $(srcdir)/gdk.defs \
		 $(srcdir)/gtk-extrafuncs.defs $(srcdir)/gtk.override
	-chmod a+w $(srcdir)
	cd $(srcdir) \
	&& $(PYTHON) ../codegen/codegen.py -o gtk.override -p pygtk gtk.defs > gen-gtk.c \
	&& cp gen-gtk.c gtk.c \
	&& rm -f gen-gtk.c

$(srcdir)/libglade.c: $(srcdir)/libglade.defs $(srcdir)/libglade.override
	-chmod a+w $(srcdir)
	cd $(srcdir) \
	&& $(PYTHON) ../codegen/codegen.py -o libglade.override -p libglade libglade.defs > gen-libglade.c \
	&& cp gen-libglade.c libglade.c \
	&& rm -f gen-libglade.c


# a hack so that gtk.c is not included in the final package.
dist-hook:
	-rm -f $(distdir)/gtk.c $(distdir)/libglade.c

EXTRA_DIST = gtk.defs gtk-extrafuncs.defs gdk.defs gtk.override \
	libglade.defs libglade.override

