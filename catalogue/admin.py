from django.contrib import admin
from .models import Bag, Soap, BaggySoap


admin.site.register(Soap)
admin.site.register(BaggySoap)


@admin.register(Bag)
class BagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bag_colour', 'label_colour', 'drawstring_colour', 'units', 'cost_price')
