/* -*- Mode: C; c-basic-offset: 4 -*- */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif
#include "pygtk-private.h"

void _pygtk_register_boxed_types(PyObject *moddict);
void register_classes(PyObject *d);

static PyMethodDef gtk_functions[] = {
    { NULL, NULL }
};

DL_EXPORT(void)
init_gtk(void)
{
    PyObject *m, *d;
    PyObject *av;
    int argc, i;
    char **argv;

    /* initialise gthread if appropriate ... */
#ifdef WITH_THREAD
    /* it is required that this function be called to enable the thread
     * safety functions */
    g_thread_init(NULL);
#endif

    /* initialise GTK ... */
    av = PySys_GetObject("argv");
    argc = PyList_Size(av);
    argv = g_new(char *, argc);
    for (i = 0; i < argc; i++)
	argv[i] = g_strdup(PyString_AsString(PyList_GetItem(av, i)));
    if (!gtk_init_check(&argc, &argv)) {
	if (argv != NULL) {
	    for (i = 0; i < argc; i++)
		g_free(argv[i]);
	    g_free(argv);
	}
	Py_FatalError("could not open display");
	return;
    }
    PySys_SetArgv(argc, argv);
    if (argv != NULL) {
	for (i = 0; i < argc; i++)
	    g_free(argv[i]);
	g_free(argv);
    }
    gtk_signal_set_funcs((GtkSignalMarshal)pygtk_signal_marshal,
			 (GtkSignalDestroy)pygtk_destroy_notify);

    /* now initialise pygtk */
    m = Py_InitModule("_gtk", gtk_functions);
    d = PyModule_GetDict(m);

    _pygtk_register_boxed_types(d);
    register_classes(d);

    if (PyErr_Occurred())
	Py_FatalError("can't initialise module _gtk");

}
