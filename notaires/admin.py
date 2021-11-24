from django.contrib import admin
from notaires.models import CabinetNotaire,Notaire

class CabinetNotaireAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'telephone', 'email', 'address','city',)
    search_fields = ['name']
admin.site.register(CabinetNotaire, CabinetNotaireAdmin)

class NotaireAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'email', 'phone', 'mobile', 'cabinet',)
admin.site.register(Notaire, NotaireAdmin)
