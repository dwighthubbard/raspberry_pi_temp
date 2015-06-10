from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from redis_collections import List as RedisList
import redislite


easydjango = True

# Get the redis_collections lists that the logger is
# writing to.
redisrdb = '/tmp/temp.rdb'
redis_connection = redislite.StrictRedis(redisrdb)
temp_c_list = RedisList(redis=redis_connection, key='temp_c')
temp_f_list = RedisList(redis=redis_connection, key='temp_f')


class LineChartJSONView(BaseLineChartView):
    """
    Line chart data
    """
    route = 'LineChartJSON'

    def get_labels(self):
        """
        Graph bottom labels
        """
        return range(len(temp_c_list[-10:]))

    def get_data(self):
        """Dataset to plot."""

        return [list(temp_c_list), list(temp_f_list)]


class LineChart(TemplateView):
    """
    Generate a webpage with a LineChart in it
    from the line_chart.html template.  Which
    accesses the LineChartJSON view to populate
    the data.
    """
    route = 'LineChart'
    template_name = 'chart_temp/line_chart.html'
