from django.shortcuts import render, redirect, reverse
from listing.models import Share, Commodity
from payment.models import SharePriceHistory, CommodityPriceHistory
from chartjs.views.lines import BaseLineChartView
from datetime import datetime


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

    def post(self, request):
        post_request = request.POST
        self.selected_id = post_request['selected_id']
        self.selected_name = post_request['selected_name']
        print(self.selected_id)
        print(self.selected_name)
        sharehistoriesreverse = SharePriceHistory.objects.filter(share=self.selected_id).order_by('-transaction_date', 'id')[:5]
        sharehistories = sharehistoriesreverse.reverse()
        self.data = []
        sharedata = []
        for sharehistory in sharehistories:
            print(datetime.now())
            print(sharehistory.new_price)
            sharedata = []
            sharedata.append(sharehistory.new_price)
            
        self.data.append(sharedata)
        print(self.data)
        self.providers = []
        self.providers.append([self.selected_name])
        self.labels = []
        context = self.get_context_data()
        print('post context data: ', context)

        return self.render_to_response(context)

    def get_data(self):
        """Return 3 datasets to plot."""
        return self.data


line_chart_json = LineChartJSONView.as_view()
