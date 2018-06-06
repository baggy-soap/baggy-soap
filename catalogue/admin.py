from django.contrib import admin
from .models import Bag, SoapLoaf, BaggySoap, SoapBar


@admin.register(Bag)
class BagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bag_colour', 'label_colour', 'drawstring_colour', 'units', 'cost_price')


@admin.register(SoapLoaf)
class SoapLoafAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'fragrance', 'colour', 'weight', 'units', 'cost_price')


@admin.register(SoapBar)
class SoapBarAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'fragrance', 'colour', 'units', 'cost_price', 'sell_price')


@admin.register(BaggySoap)
class BaggySoapAdmin(admin.ModelAdmin):
    list_display = ('id', 'bag_name', 'soap_name', 'units', 'cost_price', 'sell_price')
