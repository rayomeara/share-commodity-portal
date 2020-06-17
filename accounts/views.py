from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth.models import User
from payment.models import SharePurchase, CommodityPurchase, Wallet
from decimal import Decimal

# Create your views here.


def index(request):
    """ Return the index.html file """
    return render(request, 'index.html')


@login_required
def logout(request):
    """ Log the user out """
    auth.logout(request)
    messages.success(request, "You have successfully been logged out!")
    return redirect(reverse('index'))


def login(request):
    """ Return a login page """
    if request.user.is_authenticated:
        set_credit_amount(request, request.user)
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            if user:
                auth.login(user=user, request=request)
                set_credit_amount(request, user)
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "Your username or password was incorrect")            
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {"login_form": login_form})


def set_credit_amount(request, user):
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

    request.session['credit_amount'] = str(wallet.credit_amount)


def register(request):
    """ Render the registration page """
    if request.user.is_authenticated:
        set_credit_amount(request, request.user)
        return redirect(reverse('index'))

    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            if user:
                auth.login(user=user, request=request)
                set_credit_amount(request, user)
                messages.success(request, "You have been successfully registered")
                return redirect(reverse('index'))
            else:
                messages.error(request, "Unable to register your account at this time")
    else:
        registration_form = UserRegistrationForm()
    return render(request, 'registration.html', {"registration_form": registration_form})


def update_user(request):
    user = User.objects.get(email=request.user.email)
    user.username = request.POST['username']
    user.email = request.POST['email']
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']

    user.save()

    messages.success(request, "User updated")
    return redirect(reverse('portfolio'))


def delete_user(request):
    user = User.objects.get(email=request.user.email)
    username = user.username
    auth.logout(request)
    user.delete()
    messages.success(request, "User '" + username + "' has been removed from system. Please contact us to have remaining credit balance sent to you.")
    return redirect(reverse('index'))


def user_portfolio(request):
    """ The user's portfolio page """
    user = User.objects.get(email=request.user.email)
    share_purchases = SharePurchase.objects.filter(
        user=user
    )
    commodity_purchases = CommodityPurchase.objects.filter(
        user=user
    )
    share_commodity_purchases_length = len(share_purchases) + len(commodity_purchases)

    return render(request, 'portfolio.html', {"portfolio_user": user, "share_purchases": share_purchases, "commodity_purchases": commodity_purchases, "share_commodity_purchases_length": share_commodity_purchases_length})


def sell_shares(request, id):
    if not (request.POST.get('quantity')):
        messages.error(request, "Please enter a valid quantity to sell")
        return redirect(reverse('portfolio'))
    else:
        quantity = int(request.POST.get('quantity'))
        share_purchase = SharePurchase.objects.get(id=id)
        share = share_purchase.share
        new_share_price = Decimal(process_new_price(share.price, quantity, False))
        share.previous_price = share.price
        share.price = new_share_price
        share.save()
        user = User.objects.get(email=request.user.email)
        wallet_set = Wallet.objects.filter(
            user=user
        )

        wallet = wallet_set[0]
        sale_amount = quantity * share_purchase.share.price
        wallet.credit_amount += sale_amount
        wallet.save()
        request.session['credit_amount'] = str(wallet.credit_amount)
        if share_purchase.quantity == quantity:
            share_purchase.delete()
        else:
            share_purchase.quantity -= quantity
            share_purchase.save()

        messages.error(request, "You have successfully sold " + share_purchase.share.name + " options for " + str(share_purchase.share.price) + " each!")
        return redirect(reverse('current_listing'))


def sell_commodities(request, id):
    if not (request.POST.get('quantity')):
        messages.error(request, "Please enter a valid quantity to sell")
        return redirect(reverse('portfolio'))
    else:
        quantity = int(request.POST.get('quantity'))
        commodity_purchase = CommodityPurchase.objects.get(id=id)
        commodity = commodity_purchase.commodity
        new_commodity_price = Decimal(process_new_price(commodity.price, quantity, False))
        commodity.previous_price = commodity.price
        commodity.price = new_commodity_price
        commodity.save()
        user = User.objects.get(email=request.user.email)
        wallet_set = Wallet.objects.filter(
            user=user
        )

        wallet = wallet_set[0]
        sale_amount = quantity * commodity_purchase.commodity.price
        wallet.credit_amount += sale_amount
        wallet.save()
        request.session['credit_amount'] = str(wallet.credit_amount)
        if commodity_purchase.quantity == quantity:
            commodity_purchase.delete()
        else:
            commodity_purchase.quantity -= quantity
            commodity_purchase.save()

        messages.error(request, "You have successfully sold " + commodity_purchase.commodity.name + " options for " + str(commodity_purchase.commodity.price) + " each!")
        return redirect(reverse('current_listing'))


def process_new_price(price, quantity, is_purchase):
    if is_purchase:
        return '{:.2f}'.format(price + (price / 1000 * quantity))
    else:
        return '{:.2f}'.format(price - (price / 1000 * quantity))
