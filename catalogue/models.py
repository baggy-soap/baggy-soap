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
    sell_price = models.DecimalField(decimal_places=2, max_digits=4, null=True)

    def __str__(self):
        return self.name


class SoapLoaf(models.Model):
    name = models.CharField(max_length=64)
    fragrance = models.CharField(max_length=64)
    colour = models.CharField(max_length=64)

    # supplier

    ingredients = JSONField(default=list, blank=True, null=True)
    wholesale_link = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    sls_free = models.BooleanField(default=False, verbose_name="SLS Free")
    parabens_free = models.BooleanField(default=False, verbose_name="Parabens Free")
    palm_oil_free = models.BooleanField(default=False, verbose_name="Palm Oil Free")
    made_in_uk = models.BooleanField(default=False, verbose_name="Made in the UK")
    contains_essential_oils = models.BooleanField(default=False, verbose_name="Contains Essential Oils")
    vegan_friendly = models.BooleanField(default=False, verbose_name="Vegan Friendly")
    organic = models.BooleanField(default=False, verbose_name="Organic")

    weight = models.DecimalField(decimal_places=2, max_digits=4, verbose_name="Weight (in kg)")
    units = models.DecimalField(decimal_places=2, max_digits=8)
    bars_per_loaf = models.PositiveIntegerField()
    list_price = models.DecimalField(decimal_places=2, max_digits=4, help_text="Cost per loaf, excluding shipping")
    cost_price = models.DecimalField(decimal_places=2, max_digits=4, help_text="Cost per loaf, including shipping")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Soap Loaf'


class SoapBar(models.Model):
    loaf = models.OneToOneField(SoapLoaf, on_delete=models.CASCADE)

    units = models.PositiveIntegerField()

    sell_price = models.DecimalField(decimal_places=2, max_digits=4)

    image = models.ImageField(blank=True, null=True, upload_to='soap_bars')

    def __str__(self):
        return self.loaf.name

    @property
    def cost_price(self):
        return round(Decimal(self.loaf.cost_price / self.loaf.bars_per_loaf), 2)

    @property
    def name(self):
        return self.loaf.name

    @property
    def fragrance(self):
        return self.loaf.fragrance

    @property
    def colour(self):
        return self.loaf.colour

    def save(self, *args, **kwargs):
        if self.pk is None:
            bars_being_added = self.units
        else:
            current_units = SoapBar.objects.get(id=self.pk).units
            bars_being_added = self.units - current_units

        if bars_being_added > 0:
            number_of_loaves = self.loaf.units
            amount_of_loaf_cut = Decimal(bars_being_added) / Decimal(self.loaf.bars_per_loaf)
            self.loaf.units = Decimal(number_of_loaves) - Decimal(amount_of_loaf_cut)
            self.loaf.save()
        super(SoapBar, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Soap Bar'


class BaggySoap(models.Model):
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)
    soap = models.ForeignKey(SoapBar, on_delete=models.CASCADE)

    units = models.PositiveIntegerField()
    sell_price = models.DecimalField(decimal_places=2, max_digits=4)

    image = models.ImageField(blank=True, null=True, upload_to='baggy_soaps')

    @property
    def cost_price(self):
        return round(Decimal(self.bag.cost_price) + Decimal(self.soap.cost_price), 2)

    @property
    def bag_name(self):
        return self.bag.name

    @property
    def soap_name(self):
        return self.soap.name

    class Meta:
        verbose_name = 'Baggy Soap'
