from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from catalogue.models import SoapLoaf, SoapBar, BaggySoap, Bag


class SoapBarTest(TestCase):

    def setUp(self):
        self.loaf = SoapLoaf.objects.create(name='Tea Tree Essential Oil', fragrance='Tea Tree', colour='Green',
                                            weight=1, units=1, bars_per_loaf=12, list_price=9.99, cost_price=14.59)
        self.bar = SoapBar.objects.create(loaf=self.loaf, units=7, sell_price=4.99)

    def test_cost_price_returns_expected_value(self):
        self.assertEquals(1.22, float(self.bar.cost_price))

    def test_name_returns_loaf_name(self):
        self.assertEquals(self.loaf.name, self.bar.name)

    def test_fragrance_returns_loaf_fragrance(self):
        self.assertEquals(self.loaf.fragrance, self.bar.fragrance)

    def test_colour_returns_loaf_colour(self):
        self.assertEquals(self.loaf.colour, self.bar.colour)

    def test_save_on_create_reduces_amount_of_soap_loaf(self):
        loaf = SoapLoaf.objects.create(name='Lavender Essential Oil', fragrance='Lavender', colour='Purple',
                                       weight=1, units=2, bars_per_loaf=12, list_price=9.99, cost_price=14.59)
        SoapBar.objects.create(loaf=loaf, units=6, sell_price=4.99)
        loaf.refresh_from_db()
        self.assertEqual(1.5, float(loaf.units))

    def test_save_on_update_reduces_amount_of_soap_loaf_if_adding_bars(self):
        loaf = SoapLoaf.objects.create(name='Lavender Essential Oil', fragrance='Lavender', colour='Purple',
                                       weight=1, units=2, bars_per_loaf=12, list_price=9.99, cost_price=14.59)
        bar = SoapBar.objects.create(loaf=loaf, units=2, sell_price=4.99)
        loaf.refresh_from_db()
        self.assertEqual(1.83, float(loaf.units))
        bar = SoapBar.objects.get(id=bar.id)
        bar.units = 9
        bar.save()
        loaf.refresh_from_db()
        self.assertEqual(1.25, float(loaf.units))

    def test_save_on_update_does_not_increase_soap_loaf_if_reducing_bars(self):
        loaf = SoapLoaf.objects.create(name='Lavender Essential Oil', fragrance='Lavender', colour='Purple',
                                       weight=1, units=2, bars_per_loaf=12, list_price=9.99, cost_price=14.59)
        bar = SoapBar.objects.create(loaf=loaf, units=6, sell_price=4.99)
        loaf.refresh_from_db()
        self.assertEqual(1.5, float(loaf.units))
        bar = SoapBar.objects.get(id=bar.id)
        bar.units = 5
        bar.save()
        loaf.refresh_from_db()
        self.assertEqual(1.5, float(loaf.units))

    def test_cannot_create_duplicate_soap_bar_object(self):
        with self.assertRaises(IntegrityError):
            SoapBar.objects.create(loaf=self.loaf, units=27, sell_price=2.99)


class BaggySoapTest(TestCase):

    def setUp(self):
        self.loaf = SoapLoaf.objects.create(name='Tea Tree Essential Oil', fragrance='Tea Tree', colour='Green',
                                            weight=1, units=5, bars_per_loaf=12, list_price=9.99, cost_price=14.59)
        self.bar = SoapBar.objects.create(loaf=self.loaf, units=12, sell_price=4.99)
        self.bag = Bag.objects.create(name='White and Purple', bag_colour='FFFFFF', bag_material='Cotton',
                                      label_colour='65428A', label_material='Polyester', label_text='baggy soap',
                                      drawstring_colour='65428A', drawstring_material='Cotton', units='100',
                                      cost_price=0.60)
        self.baggy_soap = BaggySoap.objects.create(bag=self.bag, soap=self.bar, units=10, sell_price=7.99)

    def test_cost_price_returns_expected_value(self):
        self.assertEquals(1.82, float(self.baggy_soap.cost_price))

    def test_bag_name_returns_bag_name(self):
        self.assertEquals(self.bag.name, self.baggy_soap.bag_name)

    def test_soap_name_returns_soap_name(self):
        self.assertEquals(self.bar.name, self.baggy_soap.soap_name)

    def test_save_on_create_reduces_amount_of_bags_and_bars(self):
        loaf = SoapLoaf.objects.create(name='Lavender Essential Oil', fragrance='Lavender', colour='Purple',
                                       weight=1, units=2, bars_per_loaf=12, list_price=9.99, cost_price=14.59)
        bar = SoapBar.objects.create(loaf=loaf, units=12, sell_price=4.99)
        bag = Bag.objects.create(name='All Purple', bag_colour='65428A', bag_material='Cotton',
                                 label_colour='65428A', label_material='Polyester', label_text='baggy soap',
                                 drawstring_colour='65428A', drawstring_material='Cotton', units='100',
                                 cost_price=0.60)
        BaggySoap.objects.create(bag=bag, soap=bar, units=10, sell_price=7.99)
        bar.refresh_from_db()
        self.assertEqual(2, bar.units)
        bag.refresh_from_db()
        self.assertEqual(90, bag.units)

    def test_save_on_update_reduces_amount_of_bags_and_bars_if_adding_baggy_soaps(self):
        loaf = SoapLoaf.objects.create(name='Lavender Essential Oil', fragrance='Lavender', colour='Purple',
                                       weight=1, units=4, bars_per_loaf=12, list_price=9.99, cost_price=14.59)
        bar = SoapBar.objects.create(loaf=loaf, units=24, sell_price=4.99)
        bag = Bag.objects.create(name='All Purple', bag_colour='65428A', bag_material='Cotton',
                                 label_colour='65428A', label_material='Polyester', label_text='baggy soap',
                                 drawstring_colour='65428A', drawstring_material='Cotton', units='100',
                                 cost_price=0.60)
        baggy_soap = BaggySoap.objects.create(bag=bag, soap=bar, units=10, sell_price=7.99)
        bar.refresh_from_db()
        self.assertEqual(14, bar.units)
        bag.refresh_from_db()
        self.assertEqual(90, bag.units)
        baggy_soap = BaggySoap.objects.get(id=baggy_soap.id)
        baggy_soap.units = 18
        baggy_soap.save()
        bar.refresh_from_db()
        self.assertEqual(6, bar.units)
        bag.refresh_from_db()
        self.assertEqual(82, bag.units)

    def test_save_on_update_does_not_increase_bags_and_bars_if_reducing_baggy_soaps(self):
        loaf = SoapLoaf.objects.create(name='Lavender Essential Oil', fragrance='Lavender', colour='Purple',
                                       weight=1, units=4, bars_per_loaf=12, list_price=9.99, cost_price=14.59)
        bar = SoapBar.objects.create(loaf=loaf, units=24, sell_price=4.99)
        bag = Bag.objects.create(name='All Purple', bag_colour='65428A', bag_material='Cotton',
                                 label_colour='65428A', label_material='Polyester', label_text='baggy soap',
                                 drawstring_colour='65428A', drawstring_material='Cotton', units='100',
                                 cost_price=0.60)
        baggy_soap = BaggySoap.objects.create(bag=bag, soap=bar, units=10, sell_price=7.99)
        bar.refresh_from_db()
        self.assertEqual(14, bar.units)
        bag.refresh_from_db()
        self.assertEqual(90, bag.units)
        baggy_soap = BaggySoap.objects.get(id=baggy_soap.id)
        baggy_soap.units = 5
        baggy_soap.save()
        bar.refresh_from_db()
        self.assertEqual(14, bar.units)
        bag.refresh_from_db()
        self.assertEqual(90, bag.units)

    def test_cannot_create_duplicate_baggy_soap_object(self):
        with self.assertRaises(IntegrityError):
            BaggySoap.objects.create(bag=self.bag, soap=self.bar, units=20, sell_price=5.99)
