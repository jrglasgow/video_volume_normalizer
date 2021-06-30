#! /usr/bin/env python3

import os, sys, getopt, subprocess
import pprint, glob
import mimetypes
pp = pprint.PrettyPrinter(indent=4)


ffmpeg='/usr/bin/ffmpeg'

#
# debugging output
#
def dpm(var, var_name=False):
	if var_name:
		print('%s %s =>' % (var_name, type(var)))
	else:
		print('%s =>' % (var_name, type(var)))
	pp.pprint(var);

#
# get the volume for a single video
# 
# @param f filename
# @param vol_type string one of 'mean_volume' or 'max_volume'
#
def getVolume(f, vol_type='mean_volume'):
	result = subprocess.run([ffmpeg, '-i', f, '-af', 'volumedetect', '-f', 'null', '/dev/null'], stdout=subprocess.PIPE)
	dpm(result.stdout, 'result.stdout')
	pass

#
# output the help text
#
def help():
	print('%s <inputfile(s)>' % sys.argv[0])

def main(argv):
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		help()
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			help()
			sys.exit()
	
	files = []
	# allow for globbing
	for f in argv:
		paths = glob.glob(f, recursive=True)
		#dpm(paths, 'paths')
		print('')
		print('')
		print('')
		for p in paths:
			# only add video files to our list
			#dpm(p, 'p')
			mtype = mimetypes.guess_type(p)[0]
			#dpm(mtype, 'mtype')
			if mtype and 'video' in mtype:
				#dpm(mtype, 'mtype')
				files.append(p)
	# we have a list of files, get the volume level for each
	
	for f in files:
		vol = getVolume(f)
		dpm(vol, 'vol')
		pass
	

if __name__=='__main__':
	main(sys.argv[1:])