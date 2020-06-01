from django.shortcuts import render, redirect, reverse
from listing.models import Share, Commodity
from payment.models import SharePriceHistory, CommodityPriceHistory
from chartjs.views.lines import BaseLineChartView


def show_performance(request):
    """ A call to the show performance page including share and commodity parameters """
    shares = Share.objects.all()
    commodities = Commodity.objects.all()
    return render(request, "performance.html", {"shares": shares, "commodities": commodities})


class LineChartJSONView(BaseLineChartView):

    providers = ["Central", "Eastside", "Westside"]
    labels = ["January", "February", "March", "April", "May", "June", "July"]
    data = [[75, 44, 92, 11, 44, 95, 35], [41, 92, 18, 3, 73, 87, 92], [87, 21, 94, 3, 90, 13, 65]]

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return self.labels

    def get_providers(self):
        """Return names of datasets."""
        return self.providers

    def get_backgroundColor(self):
        return "rgba(0, 255, 0, 0.5)"

    
    def post(self, request):
        post_request = request.POST
        self.selected_id = post_request['selected_id']
        self.selected_name = post_request['selected_name']
        item_lookup = post_request['item']
        if (item_lookup == 'S'):
            itemhistories = SharePriceHistory.objects.filter(share=self.selected_id).order_by('-transaction_date', 'id')[:5][::-1]
        else:
            itemhistories = CommodityPriceHistory.objects.filter(commodity=self.selected_id).order_by('-transaction_date', 'id')[:5][::-1]
        self.data = []
        itemdata = []
        self.labels = []
        for itemhistory in itemhistories:
            itemdata.append(itemhistory.new_price)
            self.labels.append(itemhistory.transaction_date)

        self.data.append(itemdata)
        self.providers = []
        self.providers.append([self.selected_name])

        context = self.get_context_data()

        return self.render_to_response(context)

    def get_data(self):
        """Return 3 datasets to plot."""
        return self.data


line_chart_json = LineChartJSONView.as_view()
