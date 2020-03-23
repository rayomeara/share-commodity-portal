from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PaymentFinancialsForm, PaymentForm
from .models import PaymentShareItem, PaymentCommodityItem, SharePurchase, SharePriceHistory, CommodityPurchase, CommodityPriceHistory
from django.conf import settings
from django.utils import timezone
from listing.models import Share, Commodity
from django.contrib.auth.models import User
import stripe

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET

@login_required()
def process_payment(request):
    if request.method == "POST":
        payment_form = PaymentForm(request.POST)
        financials_form = PaymentFinancialsForm(request.POST)
        if payment_form.is_valid() and financials_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.date = timezone.now()
            payment.save()

            total = 0
            user = User.objects.get(email=request.user.email)
            share_order = request.session.get('share_order', {})
            for id, quantity in share_order.items():
                share = get_object_or_404(Share, pk=id)
                total += quantity * share.price
                payment_share_item = PaymentShareItem(
                    payment=payment,
                    share=share,
                    quantity=quantity
                )
                payment_share_item.save()
                new_share_price = process_new_price(share.price, quantity, True)
                share.previous_price = share.price
                share.price = new_share_price
                share.save()
                share_purchase = SharePurchase.filter(
                    user=user,
                    share=share
                )
                share_purchase.quantity = share_purchase.quantity + quantity
                share_purchase.save()
                share_price_history = SharePriceHistory(
                    share=share,
                    old_price=share.previous_price,
                    new_price=share.price
                )
                share_price_history.save()

            commodity_order = request.session.get('commodity_order', {})
            for id, quantity in commodity_order.items():
                commodity = get_object_or_404(Commodity, pk=id)
                total += quantity * commodity.price
                payment_commodity_item = PaymentCommodityItem(
                    payment=payment,
                    commodity=commodity,
                    quantity=quantity
                )
                payment_commodity_item.save()
                new_commodity_price = process_new_price(commodity.price, quantity, True)
                commodity.previous_price = commodity.price
                commodity.price = new_commodity_price
                commodity.save()
                commodity_purchase = CommodityPurchase.objects.get(
                    user=user,
                    commodity=commodity
                )
                commodity_purchase.quantity = commodity_purchase.quantity + quantity
                commodity_purchase.save()
                commodity_price_history = CommodityPriceHistory(
                    commodity=commodity,
                    old_price=commodity.previous_price,
                    new_price=commodity.price
                )
                commodity_price_history.save()

            try:
                customer = stripe.Charge.create(
                    amount=int(total * 100),
                    currency="EUR",
                    description=request.user.email,
                    card=financials_form.cleaned_data['stripe_id']
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")

            if customer.paid:
                messages.error(request, "You have successfully paid")
                request.session['share_order'] = {}
                request.session['commodity_order'] = {}
                return redirect(reverse('current_listing'))
            else:
                messages.error(request, "Unable to take payment")

        else:
            print(financials_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")

    else:
        financials_form = PaymentFinancialsForm()
        payment_form = PaymentForm()

    return render(request, "payment.html", {'payment_form': payment_form, 'payment_financials_form': financials_form, 'publishable': settings.STRIPE_PUBLISHABLE})

def process_new_price(price, quantity, is_purchase):
    if is_purchase:
        return price + (price / 1000 * quantity)
    else:
        return price - (price / 1000 * quantity)
