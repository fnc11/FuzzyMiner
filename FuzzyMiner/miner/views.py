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
    #print(file.read())

    return HttpResponse()
