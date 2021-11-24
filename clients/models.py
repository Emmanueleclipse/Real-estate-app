# -*- coding: utf-8 -*-
import uuid
from django.db import models
from news.models import News
from notaires.models import Notaire
from agents.models import Agent
from todo.models import ToDo
from agents.utils import to_ascii
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Client(models.Model):
    hot = models.BooleanField(default=True)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(auto_now=True)
    preferred_notaire = models.ForeignKey(Notaire, null=True, blank=True)
    agent = models.ForeignKey(Agent, db_index=True)
    last_contact = models.DateTimeField(null=True, blank=True)
    next_contact = models.DateField(null=True, blank=True)
    trash = models.CharField(max_length=255, null=True, blank=True)

    @property
    def name(self):
        try:
            name = ''
            surname = ''
            contacts = Contact.objects.filter(client_id=self.id).order_by('surname')
            for contact in contacts:
                if not contact.relationship or contact.relationship < 40:
                    if contact.surname and contact.surname in name and (contact.forename or contact.status):
                        name = name.replace(contact.surname,"+ %s %s" % (contact.forename if contact.forename else contact.get_status_display(), contact.surname))
                    else:
                        if name != '':
                            name += ' / '
                        if contact.forename:
                            name += contact.forename
                        elif contact.status:
                            name += contact.get_status_display()
                        if contact.surname:
                            name += ' '+contact.surname
#            name = Contact.objects.filter(client_id=self.id)[0].fullname
        except Exception as e:
            name = "Unknown (%s)" % self.id
            print str(e)
        return name

    @property
    def search(self):
        try:
            search = []
            contacts = Contact.objects.filter(client_id=self.id)
            for contact in contacts:
                search.append(contact.search);
        except Exception as e:
            print str(e)
        return ','.join(search)

    def __unicode__(self):
        return self.name

#    def save(self, *args, **kwargs):
 #       self.agent = self.request.user
  #      super(Client, self).save(*args, **kwargs)

class Contact(models.Model):
    STATUS_CHOICES = (
    ( 10, "M"),
    ( 10, "Mr"),
    ( 20, "Mme"),
    ( 20, "Mrs"),
    ( 30, "Mlle"),
    ( 40, "Dr"),
    ( 50, "Prof"),
    )

    RELATIONSHIP_CHOICES = (
    ( 10, "Partner"),
    ( 20, "Husband"),
    ( 30, "Wife"),
    ( 40, "Brother"),
    ( 50, "Sister"),
    ( 60, "Mother"),
    ( 70, "Father"),
    ( 80, "Cousin"),
    ( 90, "Friend"),
    (100, "Assistant"),
    (110, "Personal Assistant"),
    (120, "Property Manager"),
    (130, "Cleaner"),
    (999, "Other"),
    )

    LANGUAGE_CHOICES = (
    ( 'en', "Anglais"),
    ( 'fr', "Francais"),
    ( 'it', "Italien"),
    ( 'ru', "Russe"),
    )


    status = models.IntegerField(choices=STATUS_CHOICES, null=True, blank=True)
    forename = models.CharField(max_length=32, null=True, blank=True)
    surname = models.CharField(max_length=64, null=True, blank=True)
    relationship = models.IntegerField(choices=RELATIONSHIP_CHOICES, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=8, null=True, blank=True)
    client = models.ForeignKey(Client, db_index=True)
    search = models.CharField(max_length=255, null=True, blank=True, db_index=True)

    def _fullname(self,prefix,name,postfix):
        result = name
        if prefix:
            if prefix[-1] !=  "'":
                result = ' ' + result
            result = prefix + result
        if postfix:
            result = result+' '+postfix
        return unicode(result)


    @property
    def fullname(self):
        result = []
        if self.forename:
            result.append(self.forename)
        elif self.status:
            result.append(self.get_status_display())
        if self.surname:
            result.append(self.surname)
        return " ".join(result)

    def __unicode__(self):
        return self.fullname

    def save(self, *args, **kwargs):
        if hasattr(self,'name'):
            for key,value in self.STATUS_CHOICES:
                if self.name.lower().startswith(value.lower()+' '):
                    self.status = key
                    self.name = self.name[len(value):]
            elements = self.name.strip('. ').split()
            self.forename = elements.pop(0)
            self.surname = ' '.join(elements)
            del self.name
        search = to_ascii((self.forename if self.forename else '')+' '+(self.surname if self.surname else '')).lower().replace("-"," ")
            #(self.telephone.replace(" ", "") if self.telephone else '')+' '+(self.email if self.email else '')).lower()
        phones = ContactPhone.objects.filter(contact = self)
        for phone in phones:
            search += ' '+phone.number.replace(" ", "")
        emails = ContactEmail.objects.filter(contact = self)
        for email in emails:
            search += ' '+email.email
        self.search = ' '.join(search.split())
        super(Contact, self).save(*args, **kwargs)

class ContactPhone(models.Model):
    contact = models.ForeignKey(Contact, db_index=True)
    number = models.CharField(max_length=64)
    type = models.CharField(max_length=64, null=True, blank=True)

class ContactEmail(models.Model):
    contact = models.ForeignKey(Contact, db_index=True)
    email = models.CharField(max_length=64)
    type = models.CharField(max_length=64, null=True, blank=True)
    reply_to = models.BooleanField(default=False)

class ClientSearch(models.Model):
    STATUS_CHOICES = (
    ( 'appartement', "Appartement"),
    ( 'villa', "Villa"),
    ( 'commerce', "Commerce"),
    ( 'terrain', "Terrain"),
    ( 'garage', "Garage"),
    )

    client = models.ForeignKey(Client, db_index=True)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(auto_now=True)
    what = models.CharField(max_length=255,choices=STATUS_CHOICES,default='apartment')
    description = models.TextField()
    budget = models.IntegerField(null=True, blank=True)
    tags = models.CharField(max_length=255,null=True,blank=True)
    trash = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return "Recherche "+self.what+" &euro;"+"{:,}".format(self.budget)

class ClientSale(models.Model):
    STATUS_CHOICES = (
    ( 'appartement', "Appartement"),
    ( 'villa', "Villa"),
    ( 'commerce', "Commerce"),
    ( 'terrain', "Terrain"),
    ( 'garage', "Garage"),
    )

    client = models.ForeignKey(Client, db_index=True)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(auto_now=True)
    what = models.CharField(max_length=255,choices=STATUS_CHOICES,default='apartment')
    address = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    price = models.IntegerField(null=True, blank=True)
    tags = models.CharField(max_length=255,null=True,blank=True)
    trash = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        if self.price:
            return "A vendre: "+self.what+" pour &euro;"+"{:,}".format(self.price)
        return "A vendre: "+self.what

class ClientActivity(models.Model):
    CONTACT_CHOICES = (
    ( 'note', "Note"),
    ( 'email', "Email"),
    ( 'telephone', "Telephone"),
    ( 'rendezvous', "Rendez-vous"),
    ( 'passage', "Passage"),
    ( 'web', "Web site"),
    )
    client = models.ForeignKey(Client, db_index=True)
    date_created = models.DateTimeField()
    type = models.CharField(max_length=255,choices=CONTACT_CHOICES,default='note')
    description = models.TextField()

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.now()
        client = Client.objects.get(pk=self.client_id)
        client.last_contact = self.date_created
        client.save()

        display = { 'note': ['paperclip', 'Note sur'], 'email' : ['mail-reply', 'Email recu de'], 'telephone' : ['phone', 'Appelle recu de'], 'rendezvous' : ['car', 'Rendez-vous avec'], 'passage' : ['building', 'Passage de'], 'web' : ['globe', 'Info par web de'] }
        news = News(agent=client.agent,title=display[self.type][1]+' '+client.name,icon=display[self.type][0],description=self.description,url='/client/#'+str(client.id),created_date=self.date_created)
        news.save()

        super(ClientActivity, self).save(*args, **kwargs)

class ClientLead(models.Model):

    LANGUAGE_CHOICES = (
    ( 'fr', "Francais"),
    ( 'en', "Anglais"),
    ( 'it', "Italien"),
    ( 'ru', "Russe"),
    )

    client = models.ForeignKey(Client, null=True,blank=True,related_name='leadclient')
    assigned_agent = models.ForeignKey(Agent, null=True,blank=True,related_name='leadagent')
    source = models.CharField(max_length=255,null=True,blank=True)
    source_url = models.CharField(max_length=255,null=True,blank=True)
    source_id = models.CharField(max_length=255,unique=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    email = models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField(max_length=255,null=True,blank=True)
    buying = models.TextField(null=True,blank=True)
    selling = models.TextField(null=True,blank=True)
    what = models.CharField(max_length=255,null=True,blank=True)
    price = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True,blank=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=8, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.name if self.name else self.email

    def save(self, *args, **kwargs):

        contact = None
        if self.email:
            try: # see if email in ContactEmail
                contact_email = ContactEmail.objects.get(email=self.email,client__agent=self.assigned_agent)
                contact = contact_email.contact
            except:
                contact_email = None
        if self.phone:
            try:  # see if phone in ContactPhone
                contact_phone = ContactPhone.objects.get(number=self.phone,client__agent=self.assigned_agent)
                if contact == None:
                    contact = contact_phone.contact
            except:
                contact_phone = None


        if contact == None:
            client = Client(date_created=self.date_created,agent=self.assigned_agent)
            client.save()
            contact = Contact(client=client)
            contact.name = self.name
            contact.language = self.language
            contact.save()
        else:
            client = contact.client

        self.client = client

        if self.email and not contact_email:
            contactemail = ContactEmail(contact=contact,email=self.email)
            contactemail.save()
        if self.phone and not contact_phone:
            contactphone = ContactPhone(contact=contact,number=self.phone)
            contactphone.save()

        if not self.what or self.what and self.what not in ['appartement', 'villa', 'garage', 'terrain',]:
            self.what = 'appartement'
        if self.buying:
            try:
                search = ClientSearch.objects.get(client=client,what=self.what,trash=None) # fails if no search or if more than one
                if self.buying in search.description: # remove dupes
                    search.description.replace(self.buying,'')
                header = '<a href="'+self.source_url+'">Added from '+self.source+'</a>' if self.source_url else 'Added from '+self.source
                search.description += search.description + "\n\n<p>"+header+': '+self.buying
                search.budget=self.price
            except:
                search = ClientSearch(client=client,what=self.what,budget=self.price,description=self.buying,date_created=self.date_created)
            search.save()
        if self.selling:
            try:
                sale = ClientSale.objects.get(client=client,what=self.what,trash=None) # fails if no search or if more than one
            except:
                sale = ClientSale(client=client,what=self.what,price=self.price,description=self.selling,date_created=self.date_created)
                sale.save()

        if not self.source_id:
            self.source_id = uuid.uuid4()
        super(ClientLead, self).save(*args, **kwargs)

@receiver(post_save, sender=ClientLead)
def post_save_clientlead(sender, instance, created, **kwargs):
    price = (' &euro;'+"{:,}".format(int(instance.price))) if instance.price else ''
    header = "<b>%s - %s%s</b><br/>\n" % (instance.source, instance.what, price)
    header = '<a href="'+instance.source_url+'">'+header+'</a>' if instance.source_url else header
    if instance.buying:
        header = header+instance.buying
    elif instance.selling:
        header = header+instance.selling
    elif instance.notes:
        header = header+instance.notes
    activity = ClientActivity(client=instance.client,type='web',date_created=instance.date_created,description=header)
    activity.save()
    todo = ToDo(title='Contacter nouveau client '+instance.name,description=None,due_date=instance.date_created,for_client=instance.client,created_by=instance.assigned_agent,assigned_to=instance.assigned_agent)
    todo.save()
