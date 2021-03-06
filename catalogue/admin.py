from decimal import Decimal
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import SoapBag, SoapLoaf, BaggySoap, SoapBar


@admin.register(SoapBag)
class SoapBagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bag_colour', 'label_colour', 'drawstring_colour', 'units', 'cost_price')


@admin.register(SoapLoaf)
class SoapLoafAdmin(admin.ModelAdmin):
    class Media:
        css = {'all': ('css/admin/soap_loaf_admin.css',)}

    list_display = ('id', 'name', 'fragrance', 'colour', 'weight', 'units', 'cost_price')
    fields = (
        'name',
        'fragrance',
        'colour',
        'ingredients',
        'wholesale_link',
        'description',
        'sls_free',
        'parabens_free',
        'palm_oil_free',
        'made_in_uk',
        'contains_essential_oils',
        'vegan_friendly',
        'organic',
        'weight',
        'units',
        'bars_per_loaf',
        'list_price',
        'cost_price'
    )

    add_form_template = "admin/change_form.html"
    change_form_template = "admin/soap_loaf/change_form.html"

    def add_view(self, request, form_url='', extra_context=None):
        return super(SoapLoafAdmin, self).add_view(request)

    def change_view(self, request, object_id, form_url='', extra_content=None):
        self.readonly_fields = ['units']
        return super(SoapLoafAdmin, self).change_view(request, object_id)

    def response_change(self, request, obj):
        if "add_loaves" in request.POST:
            add_quantity = request.POST['add_quantity']
            obj.units += Decimal(add_quantity)
            obj.save()
            self.message_user(request, "{} loaves of soap have been added".format(add_quantity))
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


@admin.register(SoapBar)
class SoapBarAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'fragrance', 'colour', 'units', 'cost_price', 'sell_price')
    readonly_fields = ["image_display"]
    fields = ('loaf', 'units', 'sell_price', 'image_name', 'image_display')

    add_form_template = "admin/change_form.html"
    change_form_template = "admin/soap_bar/change_form.html"

    def image_display(self, obj):
        if obj.image_name:
            return mark_safe('<img src="/static/img/products/soap_bars/{name}" />'.format(name=obj.image_name))

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

    def save_model(self, request, obj, form, change):
        obj.name = obj.loaf.name
        obj.save()


@admin.register(BaggySoap)
class BaggySoapAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bag_link', 'soap_link', 'units', 'cost_price', 'sell_price')
    readonly_fields = ["image_display"]
    fields = ('bag', 'soap', 'units', 'sell_price', 'image_name', 'image_display')

    add_form_template = "admin/change_form.html"
    change_form_template = "admin/baggy_soap/change_form.html"

    def image_display(self, obj):
        if obj.image_name:
            return mark_safe('<img src="/static/img/products/baggy_soaps/{name}" />'.format(name=obj.image_name))

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

    def save_model(self, request, obj, form, change):
        obj.name = '{} with {}'.format(obj.bag_name, obj.soap_name)
        obj.save()

    def bag_link(self, obj):
        bag_admin_url = reverse('admin:catalogue_soapbag_change', args=[obj.bag.id])
        return mark_safe("<a href='{}'>{}</a>".format(bag_admin_url, obj.bag_name))
    bag_link.short_description = 'Bag name'
    bag_link.admin_order_field = 'bag__name'

    def soap_link(self, obj):
        soap_admin_url = reverse('admin:catalogue_soapbar_change', args=[obj.soap.id])
        return mark_safe("<a href='{}'>{}</a>".format(soap_admin_url, obj.soap_name))
    soap_link.short_description = 'Soap name'
    soap_link.admin_order_field = 'soap__name'
