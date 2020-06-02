from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth.models import User
from payment.models import SharePurchase, CommodityPurchase, UserCreditAmount

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
                user_credit_set = UserCreditAmount.objects.filter(
                    user=user
                )
                print(user_credit_set)
                print(user)
                if len(user_credit_set) == 0:
                    user_credit = UserCreditAmount(
                        user=user,
                        credit_amount=0.00
                    )
                    user_credit.save()
                else:
                    user_credit = user_credit_set[0]

                # request.session['user_credit'] = user_credit
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
