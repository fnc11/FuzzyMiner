from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.statistics.traces.log import case_statistics

from fuzzyminerpk.Configuration import Configuration, FilterConfig, MetricConfig
from fuzzyminerpk.Filter import NodeFilter, EdgeFilter, ConcurrencyFilter
from fuzzyminerpk.FuzzyMiner import Graph

# Create your views here.

""" Saves uploaded log file and returns its path (/log/example.xes) """
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        # get file from form data
        uploaded_file = request.FILES.get('logs_file')
        if settings.DEBUG:
            print(uploaded_file.name)
            print(uploaded_file.size)
        fs = FileSystemStorage()
        saved_file_name = fs.save(uploaded_file.name, uploaded_file)
        saved_file_url = fs.url(saved_file_name)
        return saved_file_url


def get_default_configuration():
    # defining default configuration
    node_filter = NodeFilter()
    edge_filter = EdgeFilter()
    concurrency_filter = ConcurrencyFilter()
    filter_config = FilterConfig(node_filter, edge_filter, concurrency_filter)
    metric_config1 = MetricConfig("frequency_significance", "unary")
    metric_config2 = MetricConfig("routing_significance", "unary")
    # and so on
    metric_configs = [metric_config1, metric_config2]
    fuzzy_config = Configuration(filter_config, metric_configs)
    return fuzzy_config


def launch_filter(log_file_path):
    log = xes_import_factory.apply(log_file_path)
    default_fuzzy_config = get_default_configuration()
    graph = Graph(log, default_fuzzy_config)
    variants_count = case_statistics.get_variant_statistics(log)
    variants_count = sorted(variants_count, key=lambda x: x['count'], reverse=True)
    return graph.edges_list


def handle_file(request):
    return render(request, 'inp_miner.html')


def show_result(request):
    log_file_path = upload(request)
    resp = launch_filter(settings.BASE_DIR + log_file_path)
    return render(request, 'res_miner.html', {'result': resp})
