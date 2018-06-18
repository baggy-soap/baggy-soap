from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

TRANSACTION_TYPES = (
    ('sale', 'Sale'),
    ('sample', 'Sample'),
    ('spoil', 'Spoil'),
    ('return', 'Return'),
)

RETAILERS = (
    ('amazon', 'Amazon'),
    ('website', 'Website'),
)

PAYMENT_TYPES = (
    ('cash', 'Cash'),
    ('card', 'Card'),
    ('amazon', 'Amazon'),
    ('paypal', 'PayPal'),
    ('n/a', 'N/A'),
)


class Transaction(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    product_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'product_id')

    type = models.CharField(max_length=32, choices=TRANSACTION_TYPES)
    retailer = models.CharField(max_length=32, choices=RETAILERS)
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    payment_type = models.CharField(max_length=32, choices=PAYMENT_TYPES)
