from django.contrib import admin
from .models import Payment, PaymentCommodityItem, PaymentShareItem, SharePriceHistory, SharePurchase, CommodityPriceHistory, CommodityPurchase, Wallet

# Register your models here.
class PaymentCommidityLineAdminInline(admin.TabularInline):
    model = PaymentCommodityItem

class PaymentShareLineAdminInline(admin.TabularInline):
    model = PaymentShareItem

class PaymentAdmin(admin.ModelAdmin):
    inlines = (PaymentCommidityLineAdminInline, PaymentShareLineAdminInline,)

admin.site.register(Payment, PaymentAdmin)
admin.site.register(SharePriceHistory)
admin.site.register(CommodityPriceHistory)
admin.site.register(SharePurchase)
admin.site.register(CommodityPurchase)
admin.site.register(Wallet)
