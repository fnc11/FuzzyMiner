import json

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.statistics.traces.log import case_statistics

from fuzzyminerpk.Attenuation import LinearAttenuation
from fuzzyminerpk.Configuration import Configuration, FilterConfig, MetricConfig
from fuzzyminerpk.Filter import NodeFilter, EdgeFilter, ConcurrencyFilter
from fuzzyminerpk.FuzzyMiner import Graph

# Create your views here.

""" Saves uploaded log file and returns its path (/log/example.xes) """


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        # get file from form data
        uploaded_file = request.FILES.get('file')
        if settings.DEBUG:
            print(uploaded_file.name)
            print(uploaded_file.size)
        fs = FileSystemStorage()
        saved_file_name = fs.save(uploaded_file.name, uploaded_file)
        saved_file_url = fs.url(saved_file_name)
        return HttpResponse(saved_file_url)


def get_default_configuration():
    # defining default configuration
    node_filter = NodeFilter()
    # Can specify type of edge filter you want use by giving "Fuzzy" or "Best"
    edge_filter = EdgeFilter("edge_filter", "Fuzzy", 0.5, 0.5, False, False)
    concurrency_filter = ConcurrencyFilter("concurrency_filter", True, 0.5, 0.5)
    filter_config = FilterConfig(node_filter, edge_filter, concurrency_filter)
    metric_config1 = MetricConfig("frequency_significance_unary", "unary")
    metric_config2 = MetricConfig("routing_significance_unary", "unary")
    metric_config3 = MetricConfig("frequency_significance_binary", "binary")
    metric_config4 = MetricConfig("distance_significance_binary", "binary")
    metric_config5 = MetricConfig("proximity_correlation_binary", "binary")
    metric_config6 = MetricConfig("originator_correlation_binary", "binary")
    metric_config7 = MetricConfig("endpoint_correlation_binary", "binary")
    metric_config8 = MetricConfig("datatype_correlation_binary", "binary")
    metric_config9 = MetricConfig("datavalue_correlation_binary", "binary")
    metric_configs = [metric_config1, metric_config2, metric_config3, metric_config4, metric_config5, metric_config6
        , metric_config7, metric_config8, metric_config9]
    attenuation = LinearAttenuation(7, 7)
    fuzzy_config = Configuration(filter_config, metric_configs, attenuation, 7)
    return fuzzy_config


def launch_filter(log_file_path):
    log = xes_import_factory.apply(log_file_path)
    default_fuzzy_config = get_default_configuration()
    graph = Graph(log)
    message_ret = graph.apply_config(default_fuzzy_config)
    variants_count = case_statistics.get_variant_statistics(log)
    variants_count = sorted(variants_count, key=lambda x: x['count'], reverse=True)
    return graph.data_repository.unary_weighted_values


def handle_file(request):
    return render(request, 'inp_miner.html')


@csrf_exempt
def show_result(request):
    data = json.loads(request.body)
    log_file_path = data["path"]
    resp = launch_filter(settings.BASE_DIR + log_file_path)
    return JsonResponse({'result': resp})

@csrf_exempt
def node_filter(request):
    data = json.loads(request.body)
    print('node filter')
    print('cutoff:', data['cutoff'])
    return HttpResponse()

@csrf_exempt
def edge_filter(request):
    data = json.loads(request.body)
    print('edge filter')
    print('edge transformer:', data['edge_transformer'])
    if data['edge_transformer'] == 'Fuzzy Edges':
        print('s/c ratio:', data['s/c_ratio'])
        print('cutoff:', data['cutoff'])
        print('ignore self-loops:', data['ignore_self_loops'])
        print('interpret absolute:', data['interpret_absolute'])
    return HttpResponse()

@csrf_exempt
def concurrency_filter(request):
    data = json.loads(request.body)
    print('concurrency filter')
    print('filter concurrency:', data['filter_concurrency'])
    print('preserve:', data['preserve'])
    print('balance:', data['balance'])
    return HttpResponse()

@csrf_exempt
def metrics_changed(request):
    data = json.loads(request.body)
    metrics = data['metrics']
    attenuation = data['attenuation']
    print('metrics:', metrics)
    print('attenuation:', attenuation)
    return HttpResponse()