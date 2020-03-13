from django.shortcuts import get_object_or_404
from products.models import Product


def order_contents(request):
    """ Ensures that the order contents are available when rendering every page """

    order = request.session.get('order', {})

    order_items = []
    total = 0
    product_count = 0
    for id, quantity in order.items():
        product = get_object_or_404(Product, pk=id)
        total += quantity * product.price
        product_count += quantity
        order_items.append({'id': id, 'quantity': quantity, 'product': product})

    return {'order_items': order_items, 'total': total, 'product_count': product_count}