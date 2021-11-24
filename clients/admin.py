from django.contrib import admin
from clients.models import Client,ClientSearch,ClientActivity,Contact,ContactPhone,ContactEmail,ClientLead

class ContactsPhoneInline(admin.TabularInline):
    model = ContactPhone
    extra = 1


class ContactsEmailInline(admin.TabularInline):
    model = ContactEmail
    extra = 1

class ContactAdmin(admin.ModelAdmin):
    inlines = [
        ContactsPhoneInline,
        ContactsEmailInline,
    ]
    list_display = ('__unicode__',)
admin.site.register(Contact, ContactAdmin)

class ClientSearchesInline(admin.TabularInline):
    model = ClientSearch
    extra = 0
    verbose_name_plural = "searches"

class ClientActivitiesInline(admin.TabularInline):
    model = ClientActivity
    extra = 0
    verbose_name_plural = "Activities"

class ClientAdmin(admin.ModelAdmin):
    inlines = [
        ClientSearchesInline,
        ClientActivitiesInline,
    ]
    list_display = ('__unicode__',)
admin.site.register(Client, ClientAdmin)

class ClientLeadAdmin(admin.ModelAdmin):
    list_display = ('source', 'name', 'date_created',)
    search_fields = ('source', 'name')
    ordering = ('-date_created',)
admin.site.register(ClientLead, ClientLeadAdmin)
