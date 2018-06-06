from decimal import Decimal
from django.contrib.postgres.fields import JSONField
from django.db import models

COLOURS = (
    ('65428A', 'Pantone Medium Purple U'),
    ('FFFFFF', 'White')
)


class Bag(models.Model):
    name = models.CharField(max_length=64)

    bag_colour = models.CharField(max_length=32, choices=COLOURS)
    bag_material = models.CharField(max_length=32)

    label_colour = models.CharField(max_length=30, choices=COLOURS)
    label_material = models.CharField(max_length=32)
    label_text = models.CharField(max_length=16)

    drawstring_colour = models.CharField(max_length=32, choices=COLOURS)
    drawstring_material = models.CharField(max_length=32)

    #supplier

    units = models.PositiveIntegerField()
    cost_price = models.DecimalField(decimal_places=2, max_digits=4, help_text="Cost per bag, including shipping")
    sell_price = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return self.name


class SoapLoaf(models.Model):
    name = models.CharField(max_length=64)
    fragrance = models.CharField(max_length=64)
    colour = models.CharField(max_length=64)

    ingredients = JSONField(default=list, blank=True, null=True)
    weight = models.DecimalField(decimal_places=2, max_digits=4, verbose_name="Weight (in kg)")

    #supplier

    units = models.DecimalField(decimal_places=2, max_digits=8)
    bars_per_loaf = models.PositiveIntegerField()

    cost_price = models.DecimalField(decimal_places=2, max_digits=4, help_text="Cost per loaf, including shipping")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Soap Loaf'


class SoapBar(models.Model):
    loaf = models.ForeignKey(SoapLoaf, on_delete=models.CASCADE)

    units = models.PositiveIntegerField()

    sell_price = models.DecimalField(decimal_places=2, max_digits=4)

    @property
    def cost_price(self):
        return round(Decimal(self.loaf.cost_price / self.loaf.bars_per_loaf), 2)

    def __str__(self):
        return self.loaf.name

    class Meta:
        verbose_name = 'Soap Bar'


class BaggySoap(models.Model):
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)
    soap = models.ForeignKey(SoapBar, on_delete=models.CASCADE)

    units = models.PositiveIntegerField()
    sell_price = models.DecimalField(decimal_places=2, max_digits=4)

    @property
    def cost_price(self):
        return round(Decimal(self.bag.cost_price + self.soap.cost_price), 2)

    class Meta:
        verbose_name = 'Baggy Soap'
