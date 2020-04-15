#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib.parse import unquote
import pyperclip
import time
import os

def macToWin(raw_path, mac_disk, win_disk):
    """
    raw_path: takes in a string representing the mac path
    mac_disk: string, mac disk name ('NAS' or 'NAS_2')
    win_disk: string, windows disk name ('Z' or 'X')
    returns the converted windows path
    """
    assert type(mac_disk) == str, "mac_disk is not passed properly to macToWin"
    assert type(win_disk) == str, "win_disk is not passed properly to macToWin"
    #raw_path = ' '.join(raw_path.split('%20'))
    win_path = "".join([win_disk, ':', unquote(raw_path).split(mac_disk)[1]])
    return win_path


#get the first thing from clipboard as the raw_input
raw_path = pyperclip.paste()
print ("Clipboard:", raw_path)

#if the first thing from clipboard is not a valid raw_path, ask for user input
#assuming the valid server paths only includes to 'NAS', 'NAS_2' and 'ARCHIVE'
while 'NAS' not in raw_path and 'ARCHIVE' not in raw_path and 'X' not in raw_path and 'Y' not in raw_path and 'Z' not in raw_path:
	print ("Invalid path, plz re-enter..")
	raw_path = input("What's the server path? ")

#if raw_path is already a windows path, assign raw_path to win_path
if "X:" in raw_path or "Y:" in raw_path or "Z:" in raw_path or "C:" in raw_path:
	win_path = raw_path
#if in NAS_2
elif 'NAS_2' in raw_path:
    win_path = macToWin(raw_path, 'NAS_2', 'X')
#if in NAS
elif 'NAS' in raw_path:
    win_path = macToWin(raw_path, 'NAS', 'Z')
else:
	win_path = macToWin(raw_path, 'ARCHIVE', 'Y')


#print out the path
print ("Opening file/path: " + win_path)
#open path
try:
    os.startfile(win_path)
#if error occurs, copy win_path to clipboard
except:     
    pyperclip.copy(win_path)
    print ("File/path no longer exists. Path copied to clipboard. ")
    #wait before closing the window
    time.sleep(3)