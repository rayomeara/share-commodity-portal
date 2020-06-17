from django.test import TestCase
from .models import Payment, PaymentCommodityItem, PaymentShareItem, SharePurchase, CommodityPurchase, CommodityPriceHistory, SharePriceHistory, Wallet
from listing.models import Commodity, Share
from django.utils import timezone
from django.contrib.auth.models import User

# Create your tests here.
class PaymentTests(TestCase):
    """ Here we'll define the tests that we'll run against
        our Payment model """

    def test_str(self):
        date = timezone.now()
        payment = Payment(full_name='A share',
                          id=1,
                          date=date)
        self.assertEqual(str(payment.full_name), 'A share')
        self.assertEqual(payment.id, 1)
        self.assertEqual(payment.date, date)


class PaymentCommodityItemTests(TestCase):
    """ Here we'll define the tests that we'll run against
        our PaymentCommodityItem model """

    def test_str(self):
        commodity = Commodity(name="commodity",
                              price=2.50)
        test_object = PaymentCommodityItem(quantity=50,
                                           commodity=commodity)
        self.assertEqual(str(test_object.commodity.name), "commodity")
        self.assertEqual(test_object.commodity.price, 2.50)
        self.assertEqual(test_object.quantity, 50)


class PaymentShareItemTests(TestCase):
    """ Here we'll define the tests that we'll run against
        our PaymentShareItem model """

    def test_str(self):
        share = Share(name="share",
                      price=2.50)
        test_object = PaymentShareItem(quantity=50,
                                       share=share)
        self.assertEqual(str(test_object.share.name), "share")
        self.assertEqual(test_object.share.price, 2.50)
        self.assertEqual(test_object.quantity, 50)


class WalletTests(TestCase):
    """ Here we'll define the tests that we'll run against
        our Wallet model """

    def test_str(self):
        user = User(id=100)
        test_object = Wallet(credit_amount=150,
                           user=user)           
        self.assertEqual(test_object.user.id, 100)
        self.assertEqual(test_object.credit_amount, 150)


class SharePurchaseTests(TestCase):
    """ Here we'll define the tests that we'll run against
        our PaymentCommodityItem model """

    def test_str(self):
        user = User(id=100)
        share = Share(name="share",
                      price=2.50)
        test_object = SharePurchase(user=user,
                                    share=share,
                                    quantity=500)
        self.assertEqual(test_object.user.id, 100)
        self.assertEqual(test_object.share.name, "share")
        self.assertEqual(test_object.quantity, 500)


class CommodityPurchaseTests(TestCase):
    """ Here we'll define the tests that we'll run against
        our CommodityPurchase model """

    def test_str(self):
        user = User(id=100)
        commodity = Commodity(name="commodity",
                              price=2.50)
        test_object = CommodityPurchase(user=user,
                                        commodity=commodity,
                                        quantity=500)
        self.assertEqual(test_object.user.id, 100)
        self.assertEqual(test_object.commodity.name, "commodity")
        self.assertEqual(test_object.quantity, 500)


class CommodityPriceHistoryTests(TestCase):
    """ Here we'll define the tests that we'll run against
        our CommodityPriceHistory model """

    def test_str(self):
        date = timezone.now()
        commodity = Commodity(name="commodity",
                              price=2.50)
        test_object = CommodityPriceHistory(commodity=commodity,
                                            old_price=100,
                                            new_price=200,
                                            transaction_date=date)
        self.assertEqual(test_object.commodity.name, 'commodity')
        self.assertEqual(test_object.old_price, 100)
        self.assertEqual(test_object.new_price, 200)
        self.assertEqual(test_object.transaction_date, date)


class SharePriceHistoryTests(TestCase):
    """ Here we'll define the tests that we'll run against
        our SharePriceHistory model """

    def test_str(self):
        date = timezone.now()
        share = Share(name="share",
                      price=2.50)
        test_object = SharePriceHistory(share=share,
                                        old_price=100,
                                        new_price=200,
                                        transaction_date=date)
        self.assertEqual(test_object.share.name, 'share')
        self.assertEqual(test_object.old_price, 100)
        self.assertEqual(test_object.new_price, 200)
        self.assertEqual(test_object.transaction_date, date)
