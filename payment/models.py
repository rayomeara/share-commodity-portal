from django.db import models
from listing.models import Share, Commodity

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
