# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser )
from utils import to_ascii
import requests
import os.path
from agency.s3 import S3StaticFiles
from agency.utils import create_thumbnail
from agency.settings import MEDIA_ROOT, MEDIA_URL


class CharNullField(models.CharField):
	description = "CharField that stores NULL but returns ''"
	def to_python(self, value):
		if isinstance(value, models.CharField):
			return value 
		if value==None:
			return ""
		else:
			return value
	def get_db_prep_value(self, value,connection,prepared=False):
		if value=="":
			return None
		else:
			return value

class Agency(models.Model):
	prefix = CharNullField(max_length=32, null=True, blank=True)
	name = models.CharField(max_length=64)
	postfix = CharNullField(max_length=32, null=True, blank=True)
	branch = CharNullField(max_length=64, null=True, blank=True)
	address = models.CharField(max_length=255, null=True, blank=True)
	postcode = models.CharField(max_length=8, null=True, blank=True)
	city = models.CharField(max_length=64, null=True, blank=True)
	lat_long = models.CharField(max_length=64, null=True, blank=True)
	telephone = CharNullField(max_length=64, null=True, blank=True)
	fax = CharNullField(max_length=64, null=True, blank=True)
	email = models.EmailField(max_length=255)
	web = models.URLField(max_length=255, null=True, blank=True)
	web_listing = models.URLField(max_length=255, null=True, blank=True)
	logo = models.ImageField(upload_to='agency_logos', null=True, blank=True)
	search = models.CharField(max_length=255, null=True, blank=True, db_index=True)
	owner	= models.ForeignKey('Agent',null=True, blank=True,related_name='agencyowner')

	emulis_id = models.IntegerField(null=True, blank=True)
	apimo_id = models.IntegerField(null=True, blank=True)
	fnaim_id = models.IntegerField(null=True, blank=True)
	orpi_id = models.IntegerField(null=True, blank=True)
	seloger_id = models.IntegerField(null=True, blank=True)

	class Meta:
		verbose_name_plural = "agencies"

	def sitelink(self):
		if not self.web:
			return 'no web site'
		return '<a href="'+self.web+'">web</a>'
	sitelink.allow_tags = True
	sitelink.short_description = 'Site'

	def _fullname(self,prefix,name,postfix,branch):
		result = name
		if prefix:
			if prefix[-1] !=  "'":
				result = ' ' + result
			result = prefix + result
		if postfix:
			result = result+' '+postfix
		if branch:
			result = result + ' ('+branch+')'
		return unicode(result)

	@property
	def agencyname(self):
		return self._fullname(self.prefix, self.name, self.postfix,None)

	def __unicode__(self):
		branch = '('+self.branch+')' if self.branch else ''
		return self._fullname(self.prefix, self.name, self.postfix, self.branch)

	def save(self, *args, **kwargs):
		self.branch = None if self.branch == '' else self.branch
		search = to_ascii(self.agencyname+' '+(self.branch if self.branch else '')+' '+self.address+' '+self.city+' '+(self.telephone.replace(" ", "") if self.telephone else '')+' '+(self.email if self.email else '')).lower()
		for find in [" de ", " la ", " l'", " du ", ]:
			search = search.replace(find, ' ')
		self.search = ' '.join(search.split())
		try:
			address = self.address+' '+self.postcode+' '+self.city+' France'
			r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params= {'sensor': 'false', 'address': address})
			location = r.json()['results'][0]['geometry']['location']
			self.lat_long = str(location['lat'])+','+str(location['lng'])
		except:
			raise ValueError('Unable to geocode address:'+address)
		else:
			super(Agency, self).save(*args, **kwargs)
#		do_something_else()

class AgentManager(BaseUserManager):
	def create_user(self, email, forename, surname, mobile, agency, photo, password=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=self.normalize_email(email),
			forename = forename,
			surname = surname,
			mobile = mobile,
			agency = agency,
			photo = photo,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, forename, surname, password):
		user = self.create_user(email,
			password=password,
			forename = forename,
			surname = surname,
			mobile=None, agency=None, photo=None, # don't need mobile, company and photo to set up superuser
		)
		user.is_admin = True
		user.save(using=self._db)
		return user

class Agent(AbstractBaseUser):
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
	)
	agency	= models.ForeignKey(Agency,null=True, blank=True)
	forename = models.CharField(max_length=254)
	surname = models.CharField(max_length=254)
	role = models.CharField(max_length=254, null=True, blank=True)
	mobile = models.CharField(max_length=254, null=True, blank=True)
	photo = models.ImageField(upload_to='agent_images', null=True, blank=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	public = models.BooleanField(default=True)
	search = models.CharField(max_length=255, null=True, blank=True)

	objects = AgentManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['forename','surname']

	def get_full_name(self):
		return "%s %s" % (self.forename, self.surname)

	def get_short_name(self):
		return self.forename

	def __unicode__(self):              # __unicode__ on Python 2
		return "%s %s" % (self.forename, self.surname)

	def thumbnail(self):
		return 'https://agencystatic.bienfacile.com/agent_photo/'+str(self.pk)+'.jpg'

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin

	def save(self, *args, **kwargs):
		search = to_ascii(self.forename+' '+self.surname+' '+(self.email if self.email else '')+' '+(self.mobile.replace(" ", "") if self.mobile else '')).lower()
		search = search+' '+self.agency.search
		self.search = ' '.join(search.split())
		super(Agent, self).save(*args, **kwargs)
#		do_something_else()

class MailProvider(models.Model):
	name = models.CharField(max_length=64)
	imap = models.CharField(max_length=64)
	imap_port = models.IntegerField(null=True,blank=True)
	smtp = models.CharField(max_length=64)
	smtp_port = models.IntegerField(null=True,blank=True)

	def __unicode__(self):              # __unicode__ on Python 2
		return "%s" % (self.name)


class AgentMailbox(models.Model):
	agent = models.ForeignKey(Agent)
	email = models.CharField(max_length=64)
	display_name = models.CharField(max_length=64)
	signature = models.TextField(null=True,blank=True)
	username = models.CharField(max_length=64)
	password = models.CharField(max_length=64)
	provider = models.ForeignKey(MailProvider)

	def __unicode__(self):              # __unicode__ on Python 2
		return "%s (%s)" % (self.agent, self.email)

class AgentSettings(models.Model):
	agent = models.ForeignKey(Agent)
	key = models.CharField(max_length=64)
	value = models.TextField(null=True,blank=True)

	def __unicode__(self):              # __unicode__ on Python 2
		return "%s = '%s'" % (self.key, self.value)



@receiver(post_save, sender=Agent)
def upload_agent_photo_s3(sender, instance, **kwargs):
	if instance.photo != instance.previous_photo:
		path = MEDIA_ROOT+'/'+instance.photo.url.replace(MEDIA_URL, '')
		thumb = path.replace('.jpg', '_thumb.jpg')
		size = (300, 300)
		create_thumbnail(path,thumb,size)
		s3 = S3StaticFiles()
		s3.savefile(thumb, 'agent_photo/'+str(instance.pk)+'.jpg')

@receiver(post_init, sender=Agent)
def remember_state(sender, **kwargs):
	instance = kwargs.get('instance')
	instance.previous_photo = instance.photo

class PreviousAgency(models.Model):
	agent = models.ForeignKey(Agent)
	agency = models.ForeignKey(Agency)
