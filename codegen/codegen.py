# -*- Mode: Python; py-indent-offset: 4 -*-
import sys, string
import parser, argtypes

import traceback

# have to do return type processing
functmpl = 'static PyObject *\n' + \
	   '_wrap_%(cname)s(PyObject *self, PyObject *args)\n' + \
	   '{\n' + \
	   '%(varlist)s' + \
	   '    if (!PyArg_ParseTuple(args, "%(typecodes)s:%(name)s"%(parselist)s))\n' + \
	   '        return NULL;\n' + \
	   '%(extracode)s\n' + \
	   '    %(cname)s(%(arglist)s);\n' + \
	   '    Py_INCREF(Py_None);\n' + \
	   '    return Py_None;\n' + \
	   '}\n\n'

methtmpl = 'static PyObject *\n' + \
	   '_wrap_%(cname)s(PyGtk_Object *self, PyObject *args)\n' + \
	   '{\n' + \
	   '%(varlist)s' + \
	   '    if (!PyArg_ParseTuple(args, "%(typecodes)s:%(class)s.%(name)s"%(parselist)s))\n' + \
	   '        return NULL;\n' + \
	   '%(extracode)s\n' + \
	   '    %(cname)s(%(cast)s(self->obj)%(arglist)s);\n' + \
	   '    Py_INCREF(Py_None);\n' + \
	   '    return Py_None;\n' + \
	   '}\n\n'

consttmpl = 'static PyObject *\n' + \
	    '_wrap_%(cname)s(PyGtk_Object *self, PyObject *args)\n' + \
	    '{\n' + \
	    '%(varlist)s' + \
	    '    if (!PyArg_ParseTuple(args, "%(typecodes)s:%(class)s.__init__"%(parselist)s))\n' + \
	    '        return NULL;\n' + \
	    '%(extracode)s\n' + \
	    '    self->obj = (GtkObject *)%(cname)s(%(arglist)s);\n' + \
	    '    if (!self->obj) {\n' + \
	    '        PyErr_SetString(PyExc_RuntimeError, "could not create %(class)s object");\n' + \
	    '        return NULL;\n' + \
	    '    }\n' + \
	    '    pygtk_register_wrapper((PyObject *)self);\n' + \
	    '    Py_INCREF(Py_None);\n' + \
	    '    return Py_None;\n' + \
	    '}\n\n'

methdeftmpl = '    { "%(name)s", %(cname)s, %(flags)s },\n'

typetmpl = 'PyExtensionClass Py%(class)s_Type = {\n' + \
	   '    PyObject_HEAD_INIT(NULL)\n' + \
	   '    0,				/* ob_size */\n' + \
	   '    "%(class)s",			/* tp_name */\n' + \
	   '    sizeof(PyGtk_Type),     	/* tp_basicsize */\n' + \
	   '    0,				/* tp_itemsize */\n' + \
	   '    /* methods */\n' + \
	   '    (destructor)pygtk_dealloc,	/* tp_dealloc */\n' + \
	   '    (printfunc)0,			/* tp_print */\n' + \
	   '    (getattrfunc)%(getattr)s,	/* tp_getattr */\n' + \
	   '    (setattrfunc)pygtk_setattr,	/* tp_setattr */\n' + \
	   '    (cmpfunc)pygtk_compare,		/* tp_compare */\n' + \
	   '    (reprfunc)pygtk_repr,		/* tp_repr */\n' + \
	   '    0,				/* tp_as_number */\n' + \
	   '    0,				/* tp_as_sequence */\n' + \
	   '    0,				/* tp_as_mapping */\n' + \
	   '    (hashfunc)pygtk_hash,		/* tp_hash */\n' + \
	   '    (getattrofunc)0,		/* tp_getattro */\n' + \
	   '    (setattrofunc)0,		/* tp_setattro */\n' + \
	   '    /* Space for future expansion */\n' + \
	   '    0L, 0L,\n' + \
	   '    NULL, /* Documentation string */\n' + \
	   '    METHOD_CHAIN(_Py%(class)s_methods)\n' + \
	   '};\n\n'

def write_function(funcobj, fp=sys.stdout):
    varlist = argtypes.VarList()
    parsestr = ''
    parselist = ['']
    extracode = []
    arglist = []
    
    dict = {
	'name':    funcobj.name,
	'cname':   funcobj.c_name,
	'varlist': varlist,
    }

    # handle return type ...
    for ptype, pname, pdflt, pnull in funcobj.params:
	if pdflt and '|' not in parsestr:
	    parsestr = parsestr + '|'
	handler = argtypes.matcher.get(ptype)
	parsestr = parsestr + handler.write_param(ptype, pname, pdflt, pnull,
						  varlist, parselist,
						  extracode, arglist)
    dict['typecodes'] = parsestr
    dict['parselist'] = string.join(parselist, ', ')
    dict['extracode'] = string.join(extracode, '')
    dict['arglist']   = string.join(arglist, ', ')
    fp.write(functmpl % dict)

def write_method(objname, methobj, fp=sys.stdout):
    varlist = argtypes.VarList()
    parsestr = ''
    parselist = ['']
    extracode = []
    arglist = ['']

    dict = {
	'name':    methobj.name,
	'cname':   methobj.c_name,
	'varlist': varlist,
	'class':   objname,
	'cast':    argtypes._to_upper_str(objname)[1:]
    }

    # handle return type ...
    for ptype, pname, pdflt, pnull in methobj.params:
	if pdflt and '|' not in parsestr:
	    parsestr = parsestr + '|'
	handler = argtypes.matcher.get(ptype)
	parsestr = parsestr + handler.write_param(ptype, pname, pdflt, pnull,
						  varlist, parselist,
						  extracode, arglist)
    dict['typecodes'] = parsestr
    dict['parselist'] = string.join(parselist, ', ')
    dict['extracode'] = string.join(extracode, '')
    dict['arglist']   = string.join(arglist, ', ')
    fp.write(methtmpl % dict)

def write_constructor(objname, funcobj, fp=sys.stdout):
    varlist = argtypes.VarList()
    parsestr = ''
    parselist = ['']
    extracode = []
    arglist = []

    dict = {
	'name':    funcobj.name,
	'cname':   funcobj.c_name,
	'varlist': varlist,
	'class':   objname,
	'cast':    argtypes._to_upper_str(objname)[1:]
    }

    # handle return type ...
    for ptype, pname, pdflt, pnull in funcobj.params:
	if pdflt and '|' not in parsestr:
	    parsestr = parsestr + '|'
	handler = argtypes.matcher.get(ptype)
	parsestr = parsestr + handler.write_param(ptype, pname, pdflt, pnull,
						  varlist, parselist,
						  extracode, arglist)
    dict['typecodes'] = parsestr
    dict['parselist'] = string.join(parselist, ', ')
    dict['extracode'] = string.join(extracode, '')
    dict['arglist']   = string.join(arglist, ', ')
    fp.write(functmpl % dict)

def write_class(parser, objobj, fp=sys.stdout):
    fp.write('\n/* ----------- ' + objobj.c_name + ' ----------- */\n\n')
    constructor = parser.find_constructor(objobj)
    methods = []
    if constructor:
	try:
	    write_constructor(objobj.c_name, constructor, fp)
	    methods.append(methdeftmpl %
			   { 'name':  '__init__',
			     'cname': '_wrap_' + constructor.c_name,
			     'flags': 'METH_VARARGS'})
	except:
	    sys.stderr.write('Could not write constructor for ' +
			     objobj.c_name + '\n')
	    traceback.print_exc()
    for meth in parser.find_methods(objobj):
	try:
	    write_method(objobj.c_name, meth, fp)
	    methods.append(methdeftmpl % { 'name':  meth.name,
					   'cname': meth.c_name,
					   'flags': 'METH_VARARGS'})
	except:
	    sys.stderr.write('Could not write method ' + objobj.c_name +
			     '.' + meth.name + '\n')
	    traceback.print_exc()

    # write the PyMethodDef structure
    methods.append('    { NULL, NULL, 0 }\n')
    fp.write('static PyMethodDef _Py' + objobj.c_name + '_methods[] = {\n')
    fp.write(string.join(methods, ''))
    fp.write('};\n\n')

    # write the type template
    fp.write(typetmpl % {'class': objobj.c_name, 'getattr': 'pygtk_getattr'})

def register_types(parser):
    for obj in parser.objects:
	argtypes.matcher.register_object(obj.c_name)
    for enum in parser.enums:
	if enum.deftype == 'flags':
	    argtypes.matcher.register_flag(enum.c_name)
	else:
	    argtypes.matcher.register_enum(enum.c_name)
