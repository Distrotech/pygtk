#!/usr/bin/env python
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
	   '%(handleret)s\n' + \
	   '}\n\n'
funccalltmpl = '%(cname)s(%(arglist)s)'

methtmpl = 'static PyObject *\n' + \
	   '_wrap_%(cname)s(PyGtk_Object *self, PyObject *args)\n' + \
	   '{\n' + \
	   '%(varlist)s' + \
	   '    if (!PyArg_ParseTuple(args, "%(typecodes)s:%(class)s.%(name)s"%(parselist)s))\n' + \
	   '        return NULL;\n' + \
	   '%(extracode)s\n' + \
	   '%(handleret)s\n' + \
	   '}\n\n'
methcalltmpl = '%(cname)s(%(cast)s(self->obj)%(arglist)s)'

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

methdeftmpl = '    { "%(name)s", (PyCFunction)%(cname)s, %(flags)s },\n'

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
	   '    %(methods)s\n' + \
	   '};\n\n'

def write_function(funcobj, fp=sys.stdout):
    varlist = argtypes.VarList()
    parsestr = ''
    parselist = ['']
    extracode = []
    arglist = []

    if funcobj.varargs:
        raise ValueError, "varargs functions not supported"
    
    dict = {
	'name':    funcobj.name,
	'cname':   funcobj.c_name,
	'varlist': varlist,
    }

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

    call = funccalltmpl % dict
    handler = argtypes.matcher.get(funcobj.ret)
    dict['handleret'] = handler.write_return(funcobj, varlist) % {'func': call}

    fp.write(functmpl % dict)

def write_method(objname, methobj, fp=sys.stdout):
    varlist = argtypes.VarList()
    parsestr = ''
    parselist = ['']
    extracode = []
    arglist = ['']

    if methobj.varargs:
        raise ValueError, "varargs methods not supported"
    
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

    call = methcalltmpl % dict
    handler = argtypes.matcher.get(methobj.ret)
    dict['handleret'] = handler.write_return(methobj, varlist) % {'func': call}

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
    fp.write(consttmpl % dict)

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
    dict = { 'class': objobj.c_name }
    dict['getattr'] = 'pygtk_getattr'
    if objobj.c_name == 'GtkObject':
        dict['methods'] = '{ _PyGtkObject_methods, base_object_method_chain }'
    else:
        dict['methods'] = 'METHOD_CHAIN(_Py' + dict['class'] + '_methods)'
    fp.write(typetmpl % dict)

def write_source(parser, fp=sys.stdout):
    fp.write('/* -*- Mode: C; c-basic-offset: 4 -*- */\n\n')
    fp.write('#include <Python.h>\n#include <ExtensionClass.h>\n\n')
    fp.write('/* ---------- forward type declarations ---------- */\n')
    for obj in parser.objects:
        fp.write('PyExtensionClass *Py' + obj.c_name + '_Type;\n')
    fp.write('\n')
    for obj in parser.objects:
        write_class(parser, obj)
        fp.write('\n')
    fp.write('/* intialise stuff extension classes */\n')
    fp.write('void\nregister_classes(PyObject *d)\n{\n')
    for obj in parser.objects:
        for parent in parser.objects:
            if (parent.name, parent.module) == obj.parent:
                fp.write('    PyExtensionClass_ExportSubclassSingle(d, "' +
                         obj.c_name + '", Py' + obj.c_name + '_Type, Py' +
                         parent.c_name + '_Type);\n')
                break
        else:
            fp.write('    PyExtensionClass_Export(d, "' + obj.c_name +
                     '", Py' + obj.c_name + '_Type);\n')
        fp.write('    pygtk_register_class("' + obj.c_name + '", &Py' +
                 obj.c_name + '_Type);\n')
    fp.write('}\n')

def register_types(parser):
    for obj in parser.objects:
	argtypes.matcher.register_object(obj.c_name)
    for enum in parser.enums:
	if enum.deftype == 'flags':
	    argtypes.matcher.register_flag(enum.c_name)
	else:
	    argtypes.matcher.register_enum(enum.c_name)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write('usage: codegen.py defsfile\n')
        sys.exit(1)
    p = parser.DefsParser(sys.argv[1])
    p.startParsing()
    register_types(p)
    write_source(p)
