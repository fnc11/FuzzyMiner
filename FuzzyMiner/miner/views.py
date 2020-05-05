import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from fuzzyminerpk import FuzzyMiner
from django.shortcuts import render
from django.conf import settings
import os

from pm4py.objects.log.importer.xes import factory as xes_import_factory

import os

# Create your views here.
@csrf_exempt
def upload(request):
    # get file from form data
    file = request.FILES.get('file')
    print(file.name)
    # read data, it is binary data
    print(file.read())
    return HttpResponse()


def launch_filter(logs_file):
    # log = xes_import_factory.apply('<path_to_xes_file>')
    file_path = os.path.join(settings.STATIC_ROOT, 'Road50.xes')
    log = xes_import_factory.apply(file_path)
    return log[0]


def handle_file(request):
    return render(request, 'inp_miner.html')


def show_result(request):
    logs_file = request.FILES['logs_file']
    resp = launch_filter(logs_file)
    return render(request, 'res_miner.html', {'result': resp})
