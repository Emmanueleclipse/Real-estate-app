import decimal
import pprint
# For JSON/ajax utils
from django.http import HttpResponse, JsonResponse
from agency.settings import SERVER_ENVIRONMENT
# For image utils
from PIL import Image

# JSON / Ajax utils
def JsonReport(e, msg):
	if SERVER_ENVIRONMENT == 'DEV':
		return JsonResponse({ 'message' : msg, 'error': str(e.message)+'('+str(type(e))+')' }, status=500)
	return JsonResponse({ 'error': 'Operation not permitted' }, status=500)

def JsonException(e):
	if SERVER_ENVIRONMENT == 'DEV':
		return JsonResponse({ 'message' : e.msg, 'error': str(e.message)+'('+str(type(e))+')' }, status=500)
	return JsonResponse({ 'error': 'Operation not permitted' }, status=500)

def JsonError(message):
	if SERVER_ENVIRONMENT == 'DEV':
		return JsonResponse({ 'error': unicode(message) }, status=500)
	return JsonResponse({ 'error': 'Operation not permitted' }, status=500)

def pkobject(submission):
	return int(submission.get('id')) if 'id' in submission and submission.get('id').isnumeric() else None

def atleast(submission, args):
	for arg in args:
		if arg in submission and submission[arg] != '':
			return True
	return False

def editobject(submission, item, created):
	if submission.get('edit'):
		return True
	if submission.get('delete') and not created:
		if submission.get('trash'):
			item.trash = submission.get('trash')
			if item.trash == 'confirm':
				item.delete()
			else:
				item.save()
		elif submission.get('confirm'):
			item.delete()
	return False

def setobject(submission, object, fields):
	for field in fields:
		key = field['key'] if 'key' in field else field['name']
		if 'required' in field and field['required'] == True and key not in submission:
#			print "Missing "+key
			return False
		found = submission.get(key, None) if key in submission else None
		if isinstance(found, str):
			found = found.strip()
		if found is None:
			if 'type' in field and field['type'] == 'boolean':
				found = False
		elif found == '':
			if 'required' in field and field['required'] == True:
#				print "Missing "+field['title']
				return False
			elif 'default' in field:
				found = field['default']
			else:
				found = None
		elif 'type' in field:
			if field['type'] == 'integer':
				if not found.isnumeric():
#					print field['title']+" must be a number"
					return False
				found = int(found)
			elif field['type'] == 'decimal':
				found = decimal.Decimal(found)
			elif field['type'] == 'boolean':
				if found == 'true' or found == 'True' or found == '1':
					found = True
				else:
					found = False
			elif field['type'] == 'onlynumbers': # strip out everything except numbers
				found = "".join([i for i in found if i.isdigit()])
			elif field['type'] == 'number': # strip out everything except numbers
				found = "".join([i for i in found if i.isdigit()])
				if found and len(found) > 0:
					found = int(found)
				else:
#					print field['title']+" must be a number"
					found = False
		if 'foreignkey' in field:
			field['name'] += '_id'
			if found:
				if isinstance(found, str) and not found.isnumeric():
#					print field['title']+" not found"
					return False
				found = int(found) if found != 'null' else None
		setattr(object, field['name'], found)
	return True

# Image utils

def flip_horizontal(im): return im.transpose(Image.FLIP_LEFT_RIGHT)
def flip_vertical(im): return im.transpose(Image.FLIP_TOP_BOTTOM)
def rotate_180(im): return im.transpose(Image.ROTATE_180)
def rotate_90(im): return im.transpose(Image.ROTATE_90)
def rotate_270(im): return im.transpose(Image.ROTATE_270)
def transpose(im): return rotate_90(flip_horizontal(im))
def transverse(im): return rotate_90(flip_vertical(im))
orientation_funcs = [None,
                 lambda x: x,
                 flip_horizontal,
                 rotate_180,
                 flip_vertical,
                 transpose,
                 rotate_270,
                 transverse,
                 rotate_90
                ]
def apply_orientation(im):
    """
    Extract the oritentation EXIF tag from the image, which should be a PIL Image instance,
    and if there is an orientation tag that would rotate the image, apply that rotation to
    the Image instance given to do an in-place rotation.

    :param Image im: Image instance to inspect
    :return: A possibly transposed image instance
    """

    try:
        kOrientationEXIFTag = 0x0112
        if hasattr(im, '_getexif'): # only present in JPEGs
            e = im._getexif()       # returns None if no EXIF data
            if e is not None:
                #log.info('EXIF data found: %r', e)
                orientation = e[kOrientationEXIFTag]
                f = orientation_funcs[orientation]
                return f(im)
    except:
        # We'd be here with an invalid orientation value or some random error?
        pass # log.exception("Error applying EXIF Orientation tag")
    return im

def create_thumbnail(from_file, to_file, size):
		image = Image.open(from_file)
		image = apply_orientation(image)
		image.thumbnail(size, Image.ANTIALIAS)
		image.save(to_file, format='JPEG', quality=75)
