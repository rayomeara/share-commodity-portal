from django.shortcuts import get_object_or_404
from listing.models import Share, Commodity
from django.contrib.auth.models import User
from payment.models import Wallet


def order_contents(request):
    """ Ensures that the order contents are available when rendering every page """
    share_order = process_order(request, 'share_order')
    commodity_order = process_order(request, 'commodity_order')
    total = share_order[1] + commodity_order[1]
    product_count = share_order[2] + commodity_order[2]
    if not request.user.is_anonymous:
        user = User.objects.get(email=request.user.email)
        wallet_set = Wallet.objects.filter(
            user=user
        )
        if len(wallet_set) == 0:
            wallet = Wallet(
                user=user,
                credit_amount=0.00
            )
            wallet.save()
        else:
            wallet = wallet_set[0]

        return {'share_order_items': share_order[0],
                'commodity_order_items': commodity_order[0],
                'total': total, 'product_count': product_count,
                'credit_amount': wallet.credit_amount}
    else:
        return {'share_order_items': share_order[0],
                'commodity_order_items': commodity_order[0],
                'total': total, 'product_count': product_count,
                'credit_amount': 0}


def process_order(request, order_type):
    # create the figures that are used to process each order item in the order
    order = request.session.get(order_type, {})
    order_items = []
    total = 0
    product_count = 0
    for id, quantity in order.items():
        if order_type == 'share_order':
            item = get_object_or_404(Share, pk=id)
        else:
            item = get_object_or_404(Commodity, pk=id)
        total += quantity * item.price
        product_count += quantity
        order_items.append({'id': id, 'quantity': quantity, 'item': item})

    return order_items, total, product_count
