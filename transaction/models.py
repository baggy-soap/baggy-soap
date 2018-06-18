from django.db import models

from catalogue.models import Product

TRANSACTION_TYPES = (
    ('sale', 'Sale'),
    ('sample', 'Sample'),
    ('spoil', 'Spoil'),
    ('return', 'Return'),
)

RETAILERS = (
    ('amazon', 'Amazon'),
    ('website', 'Website'),
    ('n/a', 'N/A'),
)

PAYMENT_TYPES = (
    ('cash', 'Cash'),
    ('card', 'Card'),
    ('amazon', 'Amazon'),
    ('paypal', 'PayPal'),
    ('n/a', 'N/A'),
)


class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    type = models.CharField(max_length=32, choices=TRANSACTION_TYPES)
    retailer = models.CharField(max_length=32, choices=RETAILERS)
    description = models.TextField(blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    payment_type = models.CharField(max_length=32, choices=PAYMENT_TYPES)

    @property
    def product_name(self):
        return '{}'.format(self.product.content_object.name)
