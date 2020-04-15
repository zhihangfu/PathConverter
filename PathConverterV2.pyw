"""
V2: added GUI based on tkinter
"""

from urllib.parse import unquote
import os
from sys import platform
from tkinter import *

# system check
if platform == "win32":
	font = "Arial"
	fsize = 12
	wsize = '400x150'
	bWidth = 2
	p = 3  #padding of cells
else: 
	font = "Futura"
	fsize = 14
	wsize = '280x135'
	bWidth = 0.5
	p = 0  #padding of cells


def convertPath(raw_path):
	"""
	convert a given path into Windows Format
	"""
	# server mapping, device specific
	def macToWin(raw_path, true_disk, win_disk):
	    """
	    raw_path: takes in a string representing the mac path
	    true_disk: string, mac disk name ('NAS' or 'NAS_2')
	    win_disk: string, windows disk name ('Z' or 'X')
	    returns the converted windows path
	    """
	    assert type(true_disk) == str, "true_disk is not passed properly to macToWin"
	    assert type(win_disk) == str, "win_disk is not passed properly to macToWin"
	    win_path = "".join([win_disk, ':', unquote(raw_path).split(true_disk)[1]])
	    return win_path

	raw_path = raw_path.strip()
	map = {'NAS':'Z', 'NAS_2':'X', 'ARCHIVE':'Y'}
	#if raw_path is already a windows path, directly assign it to win_path, otherwise convert
	if "X:" in raw_path or "Y:" in raw_path or "Z:" in raw_path or "C:" in raw_path or "D:" in raw_path:
		win_path = raw_path
	else:
		win_path = 'error'
		for disk in map:
			if disk in raw_path: win_path = macToWin(raw_path, disk, map[disk])
	
	return win_path

def openPath():
	"""
	open a given path
	p: path string
	"""
	win_path = convertPath(txt1.get("1.0",END))
	txt1.delete('1.0', END)
	txt1.insert(INSERT, win_path)
	try:
	    os.startfile(win_path)
	except:
	    s1.set("Invalid path, please re-enter:")
	else:
		s1.set('Path:')

window = Tk()
window.title("PathConvert")
window.geometry(wsize)

# path entry
s1 = StringVar()
s1.set('Path:')
lbl1 = Label(window, textvariable = s1, font = (font, fsize))
lbl1.grid(column = 0, row = 0, sticky=W+S)
txt1 = Text(window, width = 100, height = 3, borderwidth = bWidth, font = (font, fsize))
txt1.grid(column = 0, row = 1, sticky=W+E+N+S, padx = p, pady = p)

# open button
b1 = Button(window, text = "open", command = openPath, font = (font, fsize))
b1.grid(column = 0, row = 2, sticky=W+N, padx = p, pady = p)

try:
	c = window.clipboard_get() #get clipboard
except:
	pass
else:
	txt1.insert(INSERT, c)

window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=5)
window.grid_rowconfigure(2, weight=1)

window.mainloop() # keep window open
