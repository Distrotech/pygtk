#!/usr/bin/env python

#this is a simple translation of the scribble example that comes with GTK+

import sys
import ltihooks
import gtk

pixmap = None

def configure_event(widget, event):
	global pixmap
	win = widget.get_window()
	pixmap = gtk.pixmap_new(win, win.width, win.height, -1)
	gtk.draw_rectangle(pixmap, widget.get_style().white_gc, gtk.TRUE,
			   0, 0, win.width, win.height)
	return gtk.TRUE

def expose_event(widget, event):
	win = widget.get_window()
	area = event.area
	gc = widget.get_style().fg_gc[gtk.STATE_NORMAL]
	gtk.draw_pixmap(win, gc, pixmap, area[0], area[1], area[0], area[1],
			area[2], area[3])
	return gtk.FALSE

def draw_brush(widget, x, y):
	rect = (x-5, y-5, 10, 10)
	gtk.draw_rectangle(pixmap, widget.get_style().black_gc, gtk.TRUE,
			   x-5, y-5, 10, 10)
	widget.queue_draw()

def button_press_event(widget, event):
	if event.button == 1 and pixmap != None:
		draw_brush(widget, event.x, event.y)
	return gtk.TRUE

def motion_notify_event(widget, event):
	if event.is_hint:
		x, y = event.window.pointer
		state = event.window.pointer_state
	else:
		x = event.x; y = event.y
		state = event.state
	if state & gtk.GDK.BUTTON1_MASK and pixmap != None:
		draw_brush(widget, x, y)
	return gtk.TRUE

def main():
	win = gtk.GtkWindow()
	win.set_name("Test Input")
	win.connect("destroy", gtk.mainquit)
	win.set_border_width(5)

	vbox = gtk.GtkVBox(spacing=3)
	win.add(vbox)
	vbox.show()

	drawing_area = gtk.GtkDrawingArea()
	drawing_area.size(200, 200)
	vbox.pack_start(drawing_area)
	drawing_area.show()

	drawing_area.connect("expose_event", expose_event)
	drawing_area.connect("configure_event", configure_event)
	drawing_area.connect("motion_notify_event", motion_notify_event)
	drawing_area.connect("button_press_event", button_press_event)
	drawing_area.set_events(gtk.GDK.EXPOSURE_MASK |
				gtk.GDK.LEAVE_NOTIFY_MASK |
				gtk.GDK.BUTTON_PRESS_MASK |
				gtk.GDK.POINTER_MOTION_MASK |
				gtk.GDK.POINTER_MOTION_HINT_MASK)

	button = gtk.GtkButton("Quit")
	vbox.pack_start(button, expand=gtk.FALSE, fill=gtk.FALSE)
	button.connect("clicked", lambda button, win=win: win.destroy())
	button.show()
	win.show()
	gtk.main()

if __name__ == '__main__':
	main()
	
