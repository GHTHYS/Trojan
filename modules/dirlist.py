#-*- coding : utf-8 -*-
import os

def run(**args):
	print "In dirlist module:"
	dir = os.listdir(".")

	return str(dir)

