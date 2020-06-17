from django.shortcuts import render, redirect, reverse, get_object_or_404
from payment.models import Payment, PaymentShareItem, PaymentCommodityItem, SharePurchase, SharePriceHistory, CommodityPurchase, CommodityPriceHistory, Wallet
from django.utils import timezone
from listing.models import Share, Commodity
from django.contrib.auth.models import User
from django.contrib import messages
from payment.views import process_new_price


def view_order(request):
    """ A view that renders the order contents page """
    return render(request, "order.html")


def add_to_share_order(request, id):
    return add_to_order('share_order', request, id)


def add_to_commodity_order(request, id):
    return add_to_order('commodity_order', request, id)


def add_to_order(order_type, request, id):
    """ Add a quantity of the specified product to the order """
    if not (request.POST.get('quantity')):
        messages.error(request, "Please enter a valid quantity to purchase")
        return redirect(reverse('current_listing'))
    else:
        quantity = int(request.POST.get('quantity'))

        order = request.session.get(order_type, {})
        if id in order:
            order[id] = int(order[id]) + quantity
        else:
            order[id] = order.get(id, quantity)

        request.session[order_type] = order
        return redirect(reverse('view_order'))


def adjust_commodity_order(request, id):
    return adjust_order('commodity_order', request, id)


def adjust_share_order(request, id):
    return adjust_order('share_order', request, id)


def adjust_order(order_type, request, id):
    """ Adjust the quantity of the specified product to the specified amount """
    quantity = int(request.POST.get('quantity'))
    order = request.session.get(order_type, {})

    if quantity > 0:
        order[id] = quantity
    else:
        order.pop(id)

    request.session[order_type] = order
    return redirect(reverse('view_order'))


def process_no_card_payment(request):
    """ Process payment of order using non-card (credit amount) transaction"""
    user = User.objects.get(email=request.user.email)

    # create dummy Payment to indicate a simple credit transaction
    payment = Payment(
        full_name="Credit payment for " + request.user.username + " @ " + request.user.email,
        phone_number="n/a",
        country="n/a",
        postcode="n/a",
        town_or_city="n/a",
        street_address1="n/a",
        street_address2="n/a",
        date=timezone.now()
    )
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
        new_share_price = process_new_price(share.price, quantity, True)
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
        new_commodity_price = process_new_price(commodity.price, quantity, True)
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
            commodity_purchase.quantity += quantity

        commodity_purchase.save()

        # create a history of the commodity transaction for chart analysis
        commodity_price_history = CommodityPriceHistory(
            commodity=commodity,
            old_price=commodity.previous_price,
            new_price=commodity.price,
            transaction_date=timezone.now()
        )
        commodity_price_history.save()

    messages.error(request, "You have successfully completed this credit transaction for " + str(total))
    wallet_set = Wallet.objects.filter(
        user=user
    )

    # Update the credit amount and reset the order 
    # and credit amount variables
    wallet = wallet_set[0]
    wallet.credit_amount -= total
    wallet.save()
    request.session['share_order'] = {}
    request.session['commodity_order'] = {}
    request.session['credit_amount'] = str(wallet.credit_amount)
    return redirect(reverse('current_listing'))
