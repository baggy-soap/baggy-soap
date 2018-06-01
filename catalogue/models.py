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
    cost_price = models.DecimalField(decimal_places=2, max_digits=4)
    sell_price = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return self.name


class Soap(models.Model):
    name = models.CharField(max_length=64)
    fragrance = models.CharField(max_length=64)
    colour = models.CharField(max_length=64)

    #supplier

    units = models.PositiveIntegerField()
    cost_price = models.DecimalField(decimal_places=2, max_digits=4)
    sell_price = models.DecimalField(decimal_places=2, max_digits=4)


class BaggySoap(models.Model):
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)
    soap = models.ForeignKey(Soap, on_delete=models.CASCADE)

    units = models.PositiveIntegerField()
    sell_price = models.DecimalField(decimal_places=2, max_digits=4)

    def cost_price(self):
        return self.bag.cost_price + self.soap.cost_price

    class Meta:
        verbose_name = 'Baggy Soap'
