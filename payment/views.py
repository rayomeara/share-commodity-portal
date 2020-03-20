from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PaymentFinancialsForm, PaymentForm
from .models import PaymentShareItem, PaymentCommodityItem
from django.conf import settings
from django.utils import timezone
from listing.models import Share, Commodity
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

            cart = request.session.get('commodity_order', {})
            for id, quantity in cart.items():
                commodity = get_object_or_404(Commodity, pk=id)
                total += quantity * commodity.price
                payment_commodity_item = PaymentCommodityItem(
                    payment=payment,
                    commodity=commodity,
                    quantity=quantity
                )
                payment_commodity_item.save()

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
                return redirect(reverse('listing'))
            else:
                messages.error(request, "Unable to take payment")

        else:
            print(financials_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")

    else:
        financials_form = PaymentFinancialsForm()
        payment_form = PaymentForm()

    return render(request, "checkout.html", {'payment_form': payment_form, 'financials_form': financials_form, 'publishable': settings.STRIPE_PUBLISHABLE})
