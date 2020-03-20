from django.contrib import admin
from .models import Payment, PaymentCommodityItem, PaymentShareItem

# Register your models here.
class PaymentCommidityLineAdminInline(admin.TabularInline):
    model = PaymentCommodityItem

class PaymentShareLineAdminInline(admin.TabularInline):
    model = PaymentShareItem

class PaymentAdmin(admin.ModelAdmin):
    inlines = (PaymentCommidityLineAdminInline, PaymentShareLineAdminInline,)

admin.site.register(Payment, PaymentAdmin)