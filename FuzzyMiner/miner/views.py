import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def upload(request):
    # get file from form data
    file = request.FILES.get('file')
    print(file.name)
    # read data, it is binary data
    # print(file.read())
    return HttpResponse()

def node_filter(request):
    print('node filter')
    return HttpResponse()

def sc_ratio(request):
    print('sc ratio')
    return HttpResponse()

def cutoff(request):
    print('cutoff')
    return HttpResponse()

def preserve(request):
    print('preserve')
    return HttpResponse()

def balance(request):
    print('balance')
    return HttpResponse()

def metrics(request):
    print('metrics')
    return HttpResponse()