import os
import json
import logging
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from . import database
from .models import PageView

# Create your views here.
logger = logging.getLogger('django')

def index(request):
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    return render(request, 'welcome/index.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

def health(request):
    return HttpResponse(PageView.objects.count())

@csrf_exempt
def webhook(request):
    json_dict = json.loads(request.body)
    logger.info(json.dumps(json_dict, indent=4))
    return JsonResponse(json_dict)

