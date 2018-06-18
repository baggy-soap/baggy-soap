from django.contrib import admin

from transaction.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'type', 'retailer', 'amount', 'payment_type')

