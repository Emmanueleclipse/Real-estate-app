#!/usr/bin/python
from slimit import minify
import logging,gzip,os,sys
from csscompressor import compress
from s3staticutil import S3StaticFiles
from extramedia import javascript, cssmedia
import argparse

logging.disable(logging.CRITICAL)

DEPLOY = True

s3_bucket = 'agencystatic.bienfacile.com'
deploy_path = 'https://agencystatic.bienfacile.com/'

static_alias = ('/static/', '/home/sites/django/bienfacile/agency/staticfiles/')
publish_path = 'publish/'

extras = [
	'/static/endless/fonts/fontawesome-webfont.ttf',
	'/static/endless/fonts/fontawesome-webfont.woff',
]

fix_paths = [
	('../fonts/', ''),
]

def writefile(filename, contents, compression_on = False):
	print "Writing: %s" % filename
	if compression_on:
		fp_out = gzip.open(filename, 'wb')
	else:
		fp_out = open(filename, 'w')
	fp_out.write(contents)
	fp_out.close()

def writegzip(filename, contents):
	writefile(filename,contents,True)

def readfile(filename):
	print "Reading in file: %s" % filename
	with open(filename) as fp_in:
		contents = fp_in.read()
		fp_in.close()
		return contents

def fixpaths(content, paths, publish_root):
	for search,replace in paths:
		print "Doing search replace: %s to %s" % (search, replace)
		content = content.replace(search, publish_root+replace)
	return content

if __name__ == '__main__':

	parser = argparse.ArgumentParser('Deploy bienFacile agency assets')
	parser.add_argument('--deploy', action="store_true", default=False, dest='deploy', help='Deploy assets to S3 bucket')
	parser.add_argument('--admin', action="store_true", default=False, dest='admin', help='Also copy Django admin to S3 bucket')
	parser.add_argument('--images', action="store_true", default=False, dest='images', help='Copy images to S3, do nothing else')
	args = parser.parse_args()
	DEPLOY = True if args.deploy == True else False
	ADMIN = True if args.admin == True else False
	IMAGES = True if args.images == True else False

	s3 = S3StaticFiles(s3_bucket)

	# copy across static images to S3 then exit script
	if IMAGES:
		IMAGES_PATH = '/home/sites/django/bienfacile/agency/staticfiles/bienfacile/images/'
		for root, directories, filenames in os.walk(IMAGES_PATH):
			print "Searching directory "+root
			for filename in filenames:
				src = os.path.join(root,filename)
				target = src.replace(IMAGES_PATH,'')
				s3.savefile(src,target)
				print "Writing: "+os.path.join(root,filename).replace(IMAGES_PATH,'')
		sys.exit()

	# copy across admin js/css
	if DEPLOY and ADMIN:
		ADMIN_ROOT = '/home/sites/django/bienfacile/agency/staticfiles/'
		for root, directories, filenames in os.walk(ADMIN_ROOT+'admin'):
			for filename in filenames:
				src = os.path.join(root,filename)
				target = src.replace(ADMIN_ROOT,'')
				s3.savefile(src,target)
				if 'font' in target:
					s3.savefile(src,target.replace('admin/', ''))
				print "Writing: "+os.path.join(root,filename).replace(ADMIN_ROOT,'')


	# minify javascript
	for outputfile, files in javascript.iteritems():
		output = ''
		for jsfile in files:
			contents = readfile(jsfile['file'].replace(static_alias[0],static_alias[1]))
			output += "\n/*! %s - Author: %s, License: %s, more info: %s */\n" % (jsfile['file'][jsfile['file'].rfind('/')+1:],jsfile['author'],jsfile['license'],jsfile['url'],)
			logging.disable(logging.CRITICAL) # bug with slimit

#			output += contents
			if ('.min.' in jsfile['file']):
				output += contents
			else:
				output += minify(contents, mangle=True, mangle_toplevel=False)
			logging.disable(logging.NOTSET) # reset logging
		filename = outputfile.replace(static_alias[0],static_alias[1]+publish_path)
		if DEPLOY:
			writegzip(filename+'.gz',fixpaths(output,fix_paths,deploy_path))
			s3.savefile(filename+'.gz')
		writefile(filename, fixpaths(output,fix_paths,static_alias[0]+publish_path))
		writegzip(filename+'.gz',fixpaths(output,fix_paths,static_alias[0]+publish_path))

	# strip css
	for outputfile, files in cssmedia.iteritems():
		output = ''
		for cssfile in files:
			contents = readfile(cssfile.replace(static_alias[0],static_alias[1]))
			output += compress(contents)+"\n"
		filename = outputfile.replace(static_alias[0],static_alias[1]+publish_path)
		if DEPLOY:
			writegzip(filename+'.gz',fixpaths(output,fix_paths,deploy_path))
			s3.savefile(filename+'.gz')
		writefile(filename, fixpaths(output,fix_paths,static_alias[0]+publish_path))
		writegzip(filename+'.gz',fixpaths(output,fix_paths,static_alias[0]+publish_path))

	for filepath in extras:
		filename = static_alias[1]+publish_path+filepath[filepath.rfind('/')+1:]
		contents = readfile(filepath.replace(static_alias[0],static_alias[1]))
		writefile(filename, contents)
		writegzip(filename+'.gz', contents)
		if DEPLOY:
			s3.savefile(filename+'.gz')

