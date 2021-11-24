import boto
from boto.s3.key import Key
from boto.s3.connection import OrdinaryCallingFormat 

class S3StaticFiles:

	def __init__(self, bucket = 'agencystatic.bienfacile.com'):
		try:
			self.conn = boto.s3.connect_to_region('eu-west-1', aws_access_key_id='AKIAIADEAKOANSKRCTGQ', aws_secret_access_key='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', calling_format=OrdinaryCallingFormat())
			self.files = self.conn.get_bucket(bucket)
		except Exception, e:
			print "Failed connect to S3: %s" % e

	def key(self, key):
		return self.files.get_key(key)

	def getmeta(self, filename):
		headers = {}
		if filename[-3:] == '.gz':
			headers['Content-Encoding'] = 'gzip'
			filename = filename[:-3]
		mimetypes = { '.html' : 'text/html', '.css' : 'text/css', '.js' : 'application/x-javascript', '.ttf' : 'application/x-font-ttf', '.woff' : 'application/font-woff', }
		ext = filename[filename.rfind('.'):]
		if ext and ext in mimetypes:
			headers['Content-Type'] = mimetypes[ext]
		return headers

	def savefile(self, filename, destname = None):
		k = Key(self.files)
		keyname = filename[filename.rfind('/')+1:]
		meta = self.getmeta(keyname)
		for key,value in meta.iteritems():
			k.set_metadata(key, value)
		k.key = keyname
		k.set_contents_from_filename(filename, policy='public-read')

		mime = 'text/html'
		gzipencode = False

		if keyname[-3:] == '.gz':
			keyname = keyname[:-3]
			if destname:
				destname = destname[:-3]
			gzipencode = True
		if keyname[-4:] == '.css':
			mime = 'text/css'
		elif keyname[-3:] == '.js':
			mime = 'application/x-javascript'
		elif keyname[-4:] == '.ttf':
			mime = 'application/x-font-ttf'
		elif keyname[-5:] == '.woff':
			mime = 'application/font-woff'
		elif keyname[-5:] == '.jpeg' or keyname[-4:] == '.jpg':
			mime = 'image/jpeg'
		else:
			print "Unknown filetype: %s" % keyname
			return

		k.key = destname if destname else keyname
		if gzipencode:
			k.set_metadata('Content-Encoding', 'gzip')
		k.set_metadata('Content-Type', mime)
		k.set_contents_from_filename(filename, policy='public-read')

	def delete(self, filename):
		k = Key(self.images)
		k.key = filename
		self.images.delete_key(k)