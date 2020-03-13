from django.shortcuts import render, redirect, reverse


def view_order(request):
    """ A view that renders the order contents page """
    return render(request, "order.html")


def add_to_order(request, id):
    """ Add a quantity of the specified product to the order """
    quantity = int(request.POST.get('quantity'))

    order = request.session.get('order', {})
    if id in order:
        order[id] = int(order[id]) + quantity
    else:
        order[id] = order.get(id, quantity)

    request.session['order'] = order
    return redirect(reverse('index'))


def adjust_order(request, id):
    """ Adjust the quantity of the specified product to the specified amount """
    quantity = int(request.POST.get('quantity'))
    order = request.session.get('order', {})

    if quantity > 0:
        order[id] = quantity
    else:
        order.pop(id)

    request.session['order'] = order
    return redirect(reverse('view_order'))
