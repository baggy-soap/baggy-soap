from django.contrib import admin
from django.utils.safestring import mark_safe

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
    readonly_fields = ["image_display"]

    def image_display(self, obj):
        return mark_safe('<img src="/static/img/products/{name}" width="{width}" height="{height}" />'.format(
            name=obj.image.name,
            width=obj.image.width,
            height=obj.image.height,
        ))


@admin.register(BaggySoap)
class BaggySoapAdmin(admin.ModelAdmin):
    list_display = ('id', 'bag_name', 'soap_name', 'units', 'cost_price', 'sell_price')
    readonly_fields = ["image_display"]

    def image_display(self, obj):
        return mark_safe('<img src="/static/img/products/{name}" width="{width}" height={height} />'.format(
            name=obj.image.name,
            width=obj.image.width,
            height=obj.image.height,
        ))
