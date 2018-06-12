from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
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
    fields = ('loaf', 'units', 'sell_price', 'image', 'image_display')

    add_form_template = "admin/change_form.html"
    change_form_template = "admin/soap_bar/change_form.html"

    def image_display(self, obj):
        return mark_safe('<img src="/static/img/products/{name}" width="{width}" height="{height}" />'.format(
            name=obj.image.name,
            width=obj.image.width,
            height=obj.image.height,
        ))

    def add_view(self, request, form_url='', extra_context=None):
        return super(SoapBarAdmin, self).add_view(request)

    def change_view(self, request, object_id, form_url='', extra_content=None):
        self.readonly_fields.extend(['loaf', 'units'])
        return super(SoapBarAdmin, self).change_view(request, object_id)

    def response_change(self, request, obj):
        if "add_bars" in request.POST:
            add_quantity = request.POST['add_quantity']
            obj.units += int(add_quantity)
            obj.save()
            self.message_user(request, "{} bars of soap have been added".format(add_quantity))
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


@admin.register(BaggySoap)
class BaggySoapAdmin(admin.ModelAdmin):
    list_display = ('id', 'bag_name', 'soap_name', 'units', 'cost_price', 'sell_price')
    readonly_fields = ["image_display"]
    fields = ('bag', 'soap', 'units', 'sell_price', 'image', 'image_display')

    add_form_template = "admin/change_form.html"
    change_form_template = "admin/baggy_soap/change_form.html"

    def image_display(self, obj):
        return mark_safe('<img src="/static/img/products/{name}" width="{width}" height={height} />'.format(
            name=obj.image.name,
            width=obj.image.width,
            height=obj.image.height,
        ))

    def add_view(self, request, form_url='', extra_context=None):
        return super(BaggySoapAdmin, self).add_view(request)

    def change_view(self, request, object_id, form_url='', extra_content=None):
        self.readonly_fields.extend(['bag', 'soap', 'units'])
        return super(BaggySoapAdmin, self).change_view(request, object_id)

    def response_change(self, request, obj):
        if "add_baggy_soaps" in request.POST:
            add_quantity = request.POST['add_quantity']
            obj.units += int(add_quantity)
            obj.save()
            self.message_user(request, "{} Baggy Soaps have been added".format(add_quantity))
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)
