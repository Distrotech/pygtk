# -*- Mode: Python; py-indent-offset: 4 -*-

# this file contains code for loading up an override file.  The override file
# provides implementations of functions where the code generator could not
# do its job correctly.

import sys, string

class Overrides:
	def __init__(self, fp=sys.stdin):
		self.ignores = {}
		self.overrides = {}
		if fp == None: return
		# read all the components of the file ...
		bufs = map(string.strip, string.split(fp.read(), '%%'))
		if buf == ['']: return
		for buf in bufs:
			self.__parse_override(buf)
	def __parse_override(self, buffer):
		pos = string.find(buffer, '\n')
		if pos:
			line = buffer[:pos]
			rest = buffer[pos+1:]
		else:
			line = buffer ; rest = ''
		words = string.split(line)
		if words[0] == 'ignore':
			for func in words[1:]: self.ignores[func] = 1
			for func in string.split(rest): self.ignores[func] = 1
		elif words[0] == 'override':
			func = words[1]
			self.overrides[func] = rest

	def is_ignored(self, name):
		return self.ignores.has_key(name)
	def is_overriden(self, name):
		return self.overrides.has_key(name)
	def override(self, name):
		return self.overrides[name]
