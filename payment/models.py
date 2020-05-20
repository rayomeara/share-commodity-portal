from django.db import models
from listing.models import Share, Commodity
from django.contrib.auth.models import User

# Create your models here.
class Payment(models.Model):
    full_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    country = models.CharField(max_length=40, blank=False)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, blank=False)
    street_address1 = models.CharField(max_length=40, blank=False)
    street_address2 = models.CharField(max_length=40, blank=False)
    country = models.CharField(max_length=40, blank=False)
    date = models.DateField()

    def __str__(self):
        return "{0}-{1}-{2}".format(self.id, self.date, self.full_name)

class PaymentShareItem(models.Model):
    payment = models.ForeignKey(Payment, null=False)
    share = models.ForeignKey(Share, null=False)
    quantity = models.IntegerField(blank=False)

    def __str__(self):
        return "{0} {1} @ {2}".format(self.quantity, self.share.name, self.share.price)

class PaymentCommodityItem(models.Model):
    payment = models.ForeignKey(Payment, null=False)
    commodity = models.ForeignKey(Commodity, null=False)
    quantity = models.IntegerField(blank=False)

    def __str__(self):
        return "{0} {1} @ {2}".format(self.quantity, self.commodity.name, self.commodity.price)

class SharePurchase(models.Model):
    user = models.ForeignKey(User, null=False)
    share = models.ForeignKey(Share, null=False)
    quantity = models.IntegerField(blank=False)

    def __str__(self):
        return "{0} : {1} {2}".format(self.user.id, self.quantity, self.share.name)

class CommodityPurchase(models.Model):
    user = models.ForeignKey(User, null=False)
    commodity = models.ForeignKey(Commodity, null=False)
    quantity = models.IntegerField(blank=False)

    def __str__(self):
        return "{0} : {1} {2}".format(self.user.id, self.quantity, self.commodity.name)

class SharePriceHistory(models.Model):
    share = models.ForeignKey(Share, null=False)
    old_price = models.DecimalField(max_digits=6, decimal_places=2)
    new_price = models.DecimalField(max_digits=6, decimal_places=2)
    transaction_date = models.DateField()

    def __str__(self):
        return "{0} : {1} {2}: {3}".format(self.share.name, self.old_price, self.new_price, self.transaction_date)

class CommodityPriceHistory(models.Model):
    commodity = models.ForeignKey(Commodity, null=False)
    old_price = models.DecimalField(max_digits=6, decimal_places=2)
    new_price = models.DecimalField(max_digits=6, decimal_places=2)
    transaction_date = models.DateField()

    def __str__(self):
        return "{0} : {1} {2} : {3}".format(self.commodity.name, self.old_price, self.new_price, self.transaction_date)
