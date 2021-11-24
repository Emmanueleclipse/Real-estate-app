from django.contrib import admin
from sales.models import Sale, SaleOffer, SaleCommission

class SaleOfferInline(admin.TabularInline):
    model = SaleOffer
    extra = 1


class SaleCommissionInline(admin.TabularInline):
    model = SaleCommission
    extra = 1


class SaleAdmin(admin.ModelAdmin):

    inlines = [
        SaleOfferInline,
        SaleCommissionInline,
    ]

    list_display = ('buyer', 'seller', 'address', 'sale_price',)
    fieldsets = (
        (None, {'fields': ('buyer', 'seller', 'sale_price', )}),
        ('Property', {'fields': ('address', 'floor', 'size', 'pieces',)}),
        ('Agency', {'fields': ('agent_buyer', 'agent_seller', 'total_commission', 'agency_commission',)}),
        ('Notaires', {'fields': ('notaire_buyer', 'notaire_clerk_buyer', 'notaire_seller', 'notaire_clerk_seller',)}),
        ('Compromis', {'fields': ('compromis_sent_buyer', 'compromis_signed_buyer', 'compromis_sent_seller', 'compromis_signed_seller', 'compromis_final_signing_date',)}),
        ('Mortgage', {'fields': ('mortgage_required', 'mortgage_offer_received',)}),
        ('Closing', {'fields': ('sale_lost', 'signing_date', 'signing_done',)}),
        ('Payment', {'fields': ('commission_received_agency', 'commission_received_agent',)}),
        ('Before signing', {'fields': ('electricity_meter_reading', 'electricity_meter_reading_offpeak', 'water_meter_reading', 'gas_meter_reading', 'last_phone_info', )}),
        ('After signing', {'fields': ('electicity_done', 'gas_done', 'water_done', 'insurance_done', )}),
    )
    search_fields = ('buyer', 'seller')
    ordering = ('seller',)
    filter_horizontal = ()

admin.site.register(Sale, SaleAdmin)
