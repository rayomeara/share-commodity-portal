from django.shortcuts import render, redirect, reverse
from listing.models import Share, Commodity
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

    def post(self, request):
        post_request = request.POST
        self.name = post_request['name']

        self.providers = ["A", "B", "C"]
        context = self.get_context_data()
        print('post context data: ', context)

        return self.render_to_response(context)

    def get_data(self):
        """Return 3 datasets to plot."""
        return self.data


line_chart_json = LineChartJSONView.as_view()
