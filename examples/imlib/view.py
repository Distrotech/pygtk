#!/usr/bin/env python

import ltihooks

import gtk, gtk.imlib

def close(win, _event=None):
	win.hide()
	win.destroy()

def resize(win, event, im, pix):
	# note that render must be called once before each call to make_pixmap
	im.render(event.width, event.height)
	pixmap, mask = im.get_pixmap()
	pix.set(pixmap, mask)

def open_img(_b):
        file = fs.get_filename()
	try:
		im = gtk.imlib.GdkImlibImage(file)
	except RuntimeError: return
	win = gtk.GtkWindow()
	win.connect('destroy', close)
	win.connect('delete_event', close)
	win.set_title(file)
	win.set_policy(gtk.TRUE, gtk.TRUE, gtk.FALSE)
	im.render()
	pixmap, mask = im.get_pixmap()
	pix = gtk.GtkPixmap(pixmap, mask)
	win.connect('configure_event', resize, im, pix)
	pix.show()
	win.add(pix)
	win.show()

fs = gtk.GtkFileSelection()
fs.set_title('Image Viewer')
fs.connect('destroy', gtk.mainquit)
fs.connect('delete_event', gtk.mainquit)

label = fs.ok_button.children()[0]
label.set_text('View')
fs.ok_button.connect('clicked', open_img)

label = fs.cancel_button.children()[0]
label.set_text('Quit')
fs.cancel_button.connect('clicked', gtk.mainquit)

fs.show()

gtk.mainloop()
