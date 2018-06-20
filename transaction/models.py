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
    type = models.CharField(max_length=32, choices=TRANSACTION_TYPES)
    retailer = models.CharField(max_length=32, choices=RETAILERS)
    description = models.TextField(blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    payment_type = models.CharField(max_length=32, choices=PAYMENT_TYPES)

    @property
    def number_of_items(self):
        return sum(item.quantity for item in self.items.all())


class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.transaction.type != 'return':
            if self.pk is None:
                items_being_added = self.quantity
            else:
                current_quantity = TransactionItem.objects.get(id=self.pk).quantity
                items_being_added = self.quantity - current_quantity
            self.product.units -= items_being_added
            self.product.save()
        super(TransactionItem, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.product.units += self.quantity
        self.product.save()
        super(TransactionItem, self).delete(*args, **kwargs)
