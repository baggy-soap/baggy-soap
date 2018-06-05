from django.contrib import admin
from .models import Bag, SoapLoaf, BaggySoap, SoapBar


@admin.register(Bag)
class BagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bag_colour', 'label_colour', 'drawstring_colour', 'units', 'cost_price')


@admin.register(SoapLoaf)
class SoapLoafAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'fragrance', 'colour', 'units', 'cost_price')


@admin.register(SoapBar)
class SoapBarAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'fragrance', 'colour', 'units', 'cost_price', 'sell_price')

    def name(self, obj):
        return obj.loaf.name

    def fragrance(self, obj):
        return obj.loaf.fragrance

    def colour(self, obj):
        return obj.loaf.colour


@admin.register(BaggySoap)
class BaggySoapAdmin(admin.ModelAdmin):
    list_display = ('id', 'bag_name', 'soap_name', 'units', 'cost_price', 'sell_price')

    def bag_name(self, obj):
        return obj.bag.name

    def soap_name(self, obj):
        return obj.soap.loaf.name
