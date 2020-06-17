from django.shortcuts import render
from .models import Share
from .models import Commodity



def current_listing(request):
    # Create the lists of shares/commodities to display on the listing page
    shares = Share.objects.all()
    commodities = Commodity.objects.all()
    return render(request, "listing.html", {"shares": shares, "commodities": commodities})
