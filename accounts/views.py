from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth.models import User
from payment.models import SharePurchase, CommodityPurchase, Wallet

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
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            if user:
                auth.login(user=user, request=request)
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
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "Your username or password was incorrect")            
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {"login_form": login_form})


def register(request):
    """ Render the registration page """
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have been successfully registered")
                return redirect(reverse('index'))
            else:
                messages.error(request, "Unable to register your account at this time")
    else:
        registration_form = UserRegistrationForm()
    return render(request, 'registration.html', {"registration_form": registration_form})


def user_portfolio(request):
    """ The user's portfolio page """
    user = User.objects.get(email=request.user.email)
    share_purchases = SharePurchase.objects.filter(
        user=user
    )
    commodity_purchases = CommodityPurchase.objects.filter(
        user=user
    )
    return render(request, 'portfolio.html', {"portfolio_user": user, "share_purchases": share_purchases, "commodity_purchases": commodity_purchases})


def sell_shares(request, id):
    quantity = int(request.POST.get('quantity'))
    share_purchase = SharePurchase.objects.get(id=id)
    user = User.objects.get(email=request.user.email)
    wallet_set = Wallet.objects.filter(
        user=user
    )

    wallet = wallet_set[0]
    sale_amount = quantity * share_purchase.share.price
    wallet.credit_amount += sale_amount
    request.session['credit_amount'] = str(wallet.credit_amount)
    if share_purchase.quantity == quantity:
        share_purchase.delete()
    else:
        share_purchase.quantity -= quantity
        share_purchase.save()

    messages.error(request, "You have successfully sold " + share_purchase.share.name + " options for " + share_purchase.share.price + " each!")


def sell_commodities(request, id):
    quantity = int(request.POST.get('quantity'))
    commodity_purchase = CommodityPurchase.objects.get(id=id)
    user = User.objects.get(email=request.user.email)
    wallet_set = Wallet.objects.filter(
        user=user
    )

    wallet = wallet_set[0]
    sale_amount = quantity * commodity_purchase.commodity.price
    wallet.credit_amount += sale_amount
    request.session['credit_amount'] = str(wallet.credit_amount)
    if commodity_purchase.quantity == quantity:
        commodity_purchase.delete()
    else:
        commodity_purchase.quantity -= quantity
        commodity_purchase.save()

    messages.error(request, "You have successfully sold " + commodity_purchase.commodity.name + " options for " + commodity_purchase.price + " each!")
    return redirect(reverse('current_listing'))

