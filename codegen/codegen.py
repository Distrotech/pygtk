# -*- Mode: Python; py-indent-offset: 4 -*-
import sys, string
import parser, argtypes

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

