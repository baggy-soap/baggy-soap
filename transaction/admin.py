from django import forms
from django.contrib import admin

from transaction.models import Transaction, TransactionItem


class TransactionItemInlineFormset(forms.models.BaseInlineFormSet):
    pass


class TransactionItemInline(admin.StackedInline):
    formset = TransactionItemInlineFormset
    model = TransactionItem
    extra = 1


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'type', 'number_of_items', 'amount', 'retailer', 'payment_type')
    inlines = (
        TransactionItemInline,
    )
