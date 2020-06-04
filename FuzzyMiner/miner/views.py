import json

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from .graphpool import GraphPool

from fuzzyminerpk.Attenuation import LinearAttenuation, NRootAttenuation
from fuzzyminerpk.Configuration import Configuration, FilterConfig, MetricConfig
from fuzzyminerpk.Filter import NodeFilter, EdgeFilter, ConcurrencyFilter
from fuzzyminerpk.FuzzyMiner import Graph

import time
# Create your views here.

""" Saves uploaded log file and returns its path (/log/example.xes) """

def get_ip_port(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # Whether using proxy
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # Get the real ip according proxy
    else:
        ip = request.META.get('REMOTE_ADDR')  # Get the real ip
    return ip, int(request.META.get('SERVER_PORT'))

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


def get_default_configuration(num=0):
    if num == 0:
        node_filter = NodeFilter()
        edge_filter = EdgeFilter()
        concurrency_filter = ConcurrencyFilter()
    else:
        node_filter = NodeFilter()
        edge_filter = EdgeFilter(1, 0.75, 1.0)
        concurrency_filter = ConcurrencyFilter(True, 1.0, 0.7)
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
    attenuation = NRootAttenuation(5, 2.7)
    fuzzy_config = Configuration(filter_config, metric_configs, attenuation, 5)
    return fuzzy_config


def launch_filter(log_file_path, ip, port):
    log = xes_import_factory.apply(log_file_path)
    default_fuzzy_config = get_default_configuration()
    graph = Graph(log)
    pool = GraphPool()
    id = pool.update_graph(ip, port, graph)
    start = time.perf_counter()
    fm_message = graph.apply_config(default_fuzzy_config)
    finish = time.perf_counter()
    print(f'Initial config change took {round(finish - start, 3)} seconds')
    return JsonResponse({
        "message_type": fm_message.message_type,
        "message_desc": fm_message.message_desc,
        "graph_path": fm_message.graph_path,
        "id": id
    })


def to_json(fm_message):
    return JsonResponse(
        {"message_type": fm_message.message_type,
         "message_desc": fm_message.message_desc,
         "graph_path": fm_message.graph_path
         })


def handle_file(request):
    return render(request, 'inp_miner.html')


@csrf_exempt
def show_result(request):
    data = json.loads(request.body)
    log_file_path = data["path"]
    ip, port = get_ip_port(request)
    resp = launch_filter(settings.BASE_DIR + log_file_path, ip, port)
    return resp

@csrf_exempt
def node_filter(request):
    data = json.loads(request.body)
    print('node filter')
    print('cutoff:', data['cutoff'])
    node_filter_obj = NodeFilter(cut_off=data['cutoff'])
    graph = GraphPool().get_graph_by_id(data["id"])
    start = time.perf_counter()
    fm_message = graph.apply_node_filter(node_filter_obj)
    finish = time.perf_counter()
    print(f'Node filter took {round(finish - start, 3)} seconds')
    return to_json(fm_message)


@csrf_exempt
def edge_filter(request):
    data = json.loads(request.body)
    print('edge filter')
    print('edge transformer:', data['edge_transformer'])
    if data['edge_transformer'] == 'Fuzzy Edges':
        print('s/c ratio:', data['s/c_ratio'])
        print('Preserve:', data['preserve'])
        print('ignore self-loops:', data['ignore_self_loops'])
        print('interpret absolute:', data['interpret_absolute'])
        edge_filter_obj = EdgeFilter(edge_transform=1, sc_ratio=data['s/c_ratio'], preserve=data['preserve'], ignore_self_loops=data['ignore_self_loops'], interpret_abs=data['interpret_absolute'])
    else:
        edge_filter_obj = EdgeFilter(edge_transform=0, ignore_self_loops=data['ignore_self_loops'])
    graph = GraphPool().get_graph_by_id(data['id'])
    start = time.perf_counter()
    fm_message = graph.apply_edge_filter(edge_filter_obj)
    finish = time.perf_counter()
    print(f'Edge filter took {round(finish - start, 3)} seconds')
    return to_json(fm_message)


@csrf_exempt
def concurrency_filter(request):
    data = json.loads(request.body)
    print('concurrency filter')
    print('filter concurrency:', data['filter_concurrency'])
    print('preserve:', data['preserve'])
    print('balance:', data['balance'])
    concurrency_filter_obj = ConcurrencyFilter(filter_concurrency=data['filter_concurrency'], preserve=data['preserve'], offset=data['balance'])
    graph = GraphPool().get_graph_by_id(data['id'])
    start = time.perf_counter()
    fm_message = graph.apply_concurrency_filter(concurrency_filter_obj)
    finish = time.perf_counter()
    print(f'Concurrency filter took {round(finish - start, 3)} seconds')
    return to_json(fm_message)


@csrf_exempt
def metrics_changed(request):
    data = json.loads(request.body)
    metrics_data = data['metrics']
    attenuation_data = data['attenuation']
    print("metrics data:", metrics_data)
    print("attenuation data:", attenuation_data)
    unary_metrics = metrics_data['unary_metrics']
    binary_metrics = metrics_data['binary_significance']
    binary_correlation_metrics = metrics_data['binary_correlation']
    metrics_configs = list()
    for key, value in unary_metrics.items():
        metric = MetricConfig(key, "unary", value['include'], value['invert'], value['weight'])
        metrics_configs.append(metric)
    for key, value in binary_metrics.items():
        metric = MetricConfig(key, "binary", value['include'], value['invert'], value['weight'])
        metrics_configs.append(metric)
    for key, value in binary_correlation_metrics.items():
        metric = MetricConfig(key, "binary", value['include'], value['invert'], value['weight'])
        metrics_configs.append(metric)
    if attenuation_data['selected'] == "N root with radical":
        attenuation = NRootAttenuation(attenuation_data['maximal_event_distance'], attenuation_data['radical'])
    else:
        attenuation = LinearAttenuation(attenuation_data['maximal_event_distance'],
                                        attenuation_data['maximal_event_distance'])
    graph = GraphPool().get_graph_by_id(data['id'])
    start = time.perf_counter()
    fm_message = graph.apply_metrics_config(metrics_configs, attenuation, attenuation_data['maximal_event_distance'])
    finish = time.perf_counter()
    print(f'Metrics config change took {round(finish - start, 3)} seconds')
    return to_json(fm_message)
