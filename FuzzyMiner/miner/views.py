import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from path import Path

# Create your views here.
# Hard coding the log file path
logs = Path('D:\RWTH\PM Lab\BPI Assignment 2.xes').abspath()
@csrf_exempt
def upload(request):
    # get file from form data

    file = request.FILES.get(logs)
    print(file.name)
    # read data, it is binary data
    print(file.read())
    return HttpResponse()


def launch_filter(logs):
    #log = xes_import_factory.apply('D:\RWTH\PM Lab\BPI Assignment 2.xes.gz')
    log = xes_import_factory.apply(logs)
    return log[0]


def handle_file(request):
    return render(request, 'inp_miner.html')


def show_result(request):
    logs = request.FILES['logs']
    resp = launch_filter(logs)
    return render(request, 'res_miner.html', {'result': resp})
