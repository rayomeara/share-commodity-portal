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

    providers = []
    labels = []
    data = []

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return self.labels

    def get_providers(self):
        """Return names of datasets."""
        return self.providers

    def post(self, request):
        post_request = request.POST
        self.selected_id = post_request['selected_id']
        self.selected_name = post_request['selected_name']
        item_lookup = post_request['item']
        """ To get the items from the database correctly, they are ordered in descending order by date and a top 5 subset from that result.
            This then is reversed so that the items can appear in ascending order for the graph."""
        if (item_lookup == 'S'):
            itemhistories = SharePriceHistory.objects.filter(share=self.selected_id).order_by('-transaction_date', 'id')[:5][::-1]
        else:
            itemhistories = CommodityPriceHistory.objects.filter(commodity=self.selected_id).order_by('-transaction_date', 'id')[:5][::-1]
        self.data = []
        itemdata = []
        self.labels = []
        """ for each item, append the price to the data list
            and add the date to the X-Axis label list """
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
