import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.conf import settings
import os

from pm4py.objects.log.importer.xes import factory as xes_import_factory

from fuzzyminerpk.FuzzyMiner import Graph
from fuzzyminerpk.Filter import NodeFilter, EdgeFilter, ConcurrencyFilter
from fuzzyminerpk.Configuration import Configuration, FilterConfig, MetricConfig

# Create your views here.
@csrf_exempt
def upload(request):
    # get file from form data
    file = request.FILES.get('file')
    print(file.name)
    # read data, it is binary data
    print(file.read())
    return HttpResponse()


def get_default_configuration():
    # defining default configuration
    node_filter = NodeFilter()
    edge_filter = EdgeFilter()
    concurrency_filter = ConcurrencyFilter()
    filter_config = FilterConfig(node_filter, edge_filter, concurrency_filter)
    metric_config1 = MetricConfig("frequency_significance", "unary")
    metric_config2 = MetricConfig("routing_significance", "unary")
    metric_config3 = MetricConfig("frequency_significance", "binary")
    metric_config4 = MetricConfig("distance_significance", "binary")
    metric_config5 = MetricConfig("proximity_correlation", "binary")
    metric_config6 = MetricConfig("originator_correlation", "binary")
    metric_config7 = MetricConfig("endpoint_correlation", "binary")
    metric_config8 = MetricConfig("datatype_correlation", "binary")
    metric_config9 = MetricConfig("datavalue_correlation", "binary")
    metric_configs = [metric_config1, metric_config2, metric_config3, metric_config4, metric_config5, metric_config6
                      , metric_config7, metric_config8, metric_config9]
    fuzzy_config = Configuration(filter_config, metric_configs)
    return fuzzy_config


def launch_filter(logs_file):
    # log = xes_import_factory.apply('<path_to_xes_file>')
    file_path = os.path.join(settings.STATIC_ROOT, 'Road50.xes')
    log = xes_import_factory.apply(file_path)
    default_fuzzy_config = get_default_configuration()
    graph = Graph(log, default_fuzzy_config)
    return graph.nodes_dict


def handle_file(request):
    return render(request, 'inp_miner.html')


def show_result(request):
    logs_file = request.FILES['logs_file']
    resp = launch_filter(logs_file)
    return render(request, 'res_miner.html', {'result': resp})
