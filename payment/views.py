from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PaymentFinancialsForm, PaymentForm
from .models import PaymentShareItem, PaymentCommodityItem, SharePurchase, SharePriceHistory, CommodityPurchase, CommodityPriceHistory
from django.conf import settings
from django.utils import timezone
from listing.models import Share, Commodity
from django.contrib.auth.models import User
from decimal import Decimal
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

            # process each share purchase in the order
            for id, quantity in share_order.items():
                share = get_object_or_404(Share, pk=id)
                total += quantity * share.price
                payment_share_item = PaymentShareItem(
                    payment=payment,
                    share=share,
                    quantity=quantity
                )
                payment_share_item.save()

                # calculate the new price for the share as a result of this purchase
                new_share_price = Decimal(process_new_price(share.price, quantity, True))
                share.previous_price = share.price
                share.price = new_share_price
                share.save()

                # add to the share quantity for the user
                # if one does not exist, create one
                share_purchase_set = SharePurchase.objects.filter(
                    user=user,
                    share=share
                )
                if len(share_purchase_set) == 0:
                    share_purchase = SharePurchase(
                        user=user,
                        share=share,
                        quantity=quantity
                    )
                else:
                    share_purchase = share_purchase_set[0]
                    share_purchase.quantity += quantity

                share_purchase.save()

                # create a history of the share transaction for chart analysis
                share_price_history = SharePriceHistory(
                    share=share,
                    old_price=share.previous_price,
                    new_price=share.price,
                    transaction_date=timezone.now()
                )
                share_price_history.save()

            commodity_order = request.session.get('commodity_order', {})

            # process each commodity purchase in the order
            for id, quantity in commodity_order.items():
                commodity = get_object_or_404(Commodity, pk=id)
                total += quantity * commodity.price
                payment_commodity_item = PaymentCommodityItem(
                    payment=payment,
                    commodity=commodity,
                    quantity=quantity
                )
                payment_commodity_item.save()

                # calculate the new price for the commodity as a result of this purchase
                new_commodity_price = Decimal(process_new_price(commodity.price, quantity, True))
                commodity.previous_price = commodity.price
                commodity.price = new_commodity_price
                commodity.save()

                # add to the commodity quantity for the user
                # if one does not exist, create one
                commodity_purchase_set = CommodityPurchase.objects.filter(
                    user=user,
                    commodity=commodity
                )
                if len(commodity_purchase_set) == 0:
                    commodity_purchase = CommodityPurchase(
                        user=user,
                        commodity=commodity,
                        quantity=quantity
                    )
                else:
                    commodity_purchase = commodity_purchase_set[0]
                    commodity_purchase.quantity = commodity_purchase.quantity + quantity
                commodity_purchase.save()

                # create a history of the commodity transaction for chart analysis
                commodity_price_history = CommodityPriceHistory(
                    commodity=commodity,
                    old_price=commodity.previous_price,
                    new_price=commodity.price,
                    transaction_date=timezone.now()
                )
                commodity_price_history.save()

            # create a stripe charge using the required details
            # if it fails, show an error
            # on success, clear session objects and go to listing page
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
    #calculate new price for share/commodity
    #increase for purchase, decrease for sale
    if is_purchase:
        return '{:.2f}'.format(price + (price / 1000 * quantity))
    else:
        return '{:.2f}'.format(price - (price / 1000 * quantity))
