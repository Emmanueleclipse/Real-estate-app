from django.db import models

class CabinetNotaire(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=255, null=True, blank=True)
    postcode = models.CharField(max_length=8, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    telephone = models.CharField(max_length=64, null=True, blank=True)
    fax = models.CharField(max_length=64, null=True, blank=True)
    email = models.EmailField(max_length=255)
    web = models.URLField(max_length=255, null=True, blank=True)
    search = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Notaire(models.Model):
    forename = models.CharField(max_length=32)
    surname = models.CharField(max_length=64, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=64, null=True, blank=True)
    mobile = models.CharField(max_length=64, null=True, blank=True)
    photo = models.ImageField(upload_to='notaire_photos', null=True, blank=True)
    cabinet = models.ForeignKey(CabinetNotaire)
    search = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.forename+' '+self.surname
