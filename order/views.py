from django.shortcuts import render, redirect, reverse


def view_order(request):
    """ A view that renders the order contents page """
    return render(request, "order.html")


def add_to_share_order(request, id):
    return add_to_order('share_order', request, id)


def add_to_commodity_order(request, id):
    return add_to_order('commodity_order', request, id)


def add_to_order(order_type, request, id):
    """ Add a quantity of the specified product to the order """
    quantity = int(request.POST.get('quantity'))

    order = request.session.get(order_type, {})
    if id in order:
        order[id] = int(order[id]) + quantity
    else:
        order[id] = order.get(id, quantity)

    request.session[order_type] = order
    return redirect(reverse('index'))


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