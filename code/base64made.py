#!/usr/bin/python

import sys
import base64
import getopt

lineb64 = []

def usage():
	print "Usage: base64made.py"
	print "-i --in		-input file"
	print "-o --out		-output file"
	print "-h --help	-help document"

try:
    opt, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "in=", "out="])
except getopt.GetoptError,err:
    print str(err)        
for o, a in opt:
    if o in ("-h", "--help"):
	usage()
    if o in ("-i", "--in"):
	try:
		files = open(a, "r+")
		lines = files.readlines()
		print lines
		for line in lines:
			linb64 = base64.b64encode(line)
			print linb64
			lineb64.append(linb64)
		print lineb64
		files.close()
	except Exception,err:
		print str(err)	
		files.close()
    if o in ("-o", "--in"):
	try:
		files = open(a, "w")
		for line in lineb64:	
			files.write(line)
			files.write('\n')
		files.close()
	except Exception, err:
		print str(err)
		files.close()

