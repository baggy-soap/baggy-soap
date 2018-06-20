from unittest import TestCase

from catalogue.models import SoapLoaf, SoapBar, SoapBag, BaggySoap
from transaction.models import TransactionItem, Transaction


class TransactionTest(TestCase):

    def setUp(self):
        self.loaf = SoapLoaf.objects.create(name='Tea Tree Essential Oil', fragrance='Tea Tree', colour='Green',
                                            weight=1, units=5, bars_per_loaf=12, list_price=9.99, cost_price=14.59)
        self.bar = SoapBar.objects.create(loaf=self.loaf, units=12, sell_price=4.99)
        self.bag = SoapBag.objects.create(name='White and Purple', bag_colour='FFFFFF', bag_material='Cotton',
                                          label_colour='65428A', label_material='Polyester', label_text='baggy soap',
                                          drawstring_colour='65428A', drawstring_material='Cotton', units='100',
                                          cost_price=0.60)
        self.baggy_soap = BaggySoap.objects.create(bag=self.bag, soap=self.bar, units=10, sell_price=7.99)
        self.transaction = Transaction.objects.create(type='sample', retailer='n/a', amount=0, payment_type='n/a')

    def test_number_of_items_returns_correct_amount_from_all_transaction_items(self):
        TransactionItem.objects.create(transaction=self.transaction, product=self.baggy_soap, quantity=2, price=0)
        TransactionItem.objects.create(transaction=self.transaction, product=self.bar, quantity=1, price=0)
        self.assertEqual(3, self.transaction.number_of_items)


class TransactionItemTest(TestCase):

    def setUp(self):
        self.loaf = SoapLoaf.objects.create(name='Tea Tree Essential Oil', fragrance='Tea Tree', colour='Green',
                                            weight=1, units=5, bars_per_loaf=12, list_price=9.99, cost_price=14.59)
        self.bar = SoapBar.objects.create(loaf=self.loaf, units=12, sell_price=4.99)
        self.bag = SoapBag.objects.create(name='White and Purple', bag_colour='FFFFFF', bag_material='Cotton',
                                          label_colour='65428A', label_material='Polyester', label_text='baggy soap',
                                          drawstring_colour='65428A', drawstring_material='Cotton', units='100',
                                          cost_price=0.60)
        self.baggy_soap = BaggySoap.objects.create(bag=self.bag, soap=self.bar, units=10, sell_price=7.99)
        self.transaction = Transaction.objects.create(type='sample', retailer='n/a', amount=0, payment_type='n/a')

    def test_save_on_create_reduces_amount_of_baggy_soaps(self):
        TransactionItem.objects.create(transaction=self.transaction, product=self.baggy_soap, quantity=1, price=0)
        self.baggy_soap.refresh_from_db()
        self.assertEqual(9, self.baggy_soap.units)

    def test_save_on_create_reduces_amount_of_soap_bags(self):
        self.assertEqual(90, self.bag.units)
        TransactionItem.objects.create(transaction=self.transaction, product=self.bag, quantity=1, price=0)
        self.bag.refresh_from_db()
        self.assertEqual(89, self.bag.units)

    def test_save_on_create_reduces_amount_of_soap_bars(self):
        self.assertEqual(2, self.bar.units)
        TransactionItem.objects.create(transaction=self.transaction, product=self.bar, quantity=1, price=0)
        self.bar.refresh_from_db()
        self.assertEqual(1, self.bar.units)

    def test_save_on_create_reduces_amount_of_soap_loaves(self):
        self.assertEqual(4, self.loaf.units)
        TransactionItem.objects.create(transaction=self.transaction, product=self.loaf, quantity=1,
                                       price=0)
        self.baggy_soap.refresh_from_db()
        self.assertEqual(3, self.loaf.units)

    def test_save_on_create_does_not_reduce_number_of_products_if_type_is_return(self):
        transaction = Transaction.objects.create(type='return', retailer='n/a', amount=0, payment_type='n/a')
        TransactionItem.objects.create(transaction=transaction, product=self.baggy_soap, quantity=1, price=0)
        self.baggy_soap.refresh_from_db()
        self.assertEqual(10, self.baggy_soap.units)

    def test_save_on_update_reduces_number_of_products_if_increasing_quantity(self):
        item = TransactionItem.objects.create(transaction=self.transaction, product=self.baggy_soap,
                                              quantity=1, price=0)
        self.baggy_soap.refresh_from_db()
        self.assertEqual(9, self.baggy_soap.units)
        item = TransactionItem.objects.get(id=item.id)
        item.quantity = 3
        item.save()
        self.baggy_soap.refresh_from_db()
        self.assertEqual(7, self.baggy_soap.units)

    def test_save_on_update_increases_number_of_products_if_reducing_quantity(self):
        item = TransactionItem.objects.create(transaction=self.transaction, product=self.baggy_soap,
                                              quantity=3, price=0)
        self.baggy_soap.refresh_from_db()
        self.assertEqual(7, self.baggy_soap.units)
        item = TransactionItem.objects.get(id=item.id)
        item.quantity = 1
        item.save()
        self.baggy_soap.refresh_from_db()
        self.assertEqual(9, self.baggy_soap.units)

    def test_delete_increases_number_of_products(self):
        item = TransactionItem.objects.create(transaction=self.transaction, product=self.baggy_soap,
                                              quantity=3, price=0)
        self.baggy_soap.refresh_from_db()
        self.assertEqual(7, self.baggy_soap.units)
        item = TransactionItem.objects.get(id=item.id)
        item.delete()
        self.baggy_soap.refresh_from_db()
        self.assertEqual(10, self.baggy_soap.units)
