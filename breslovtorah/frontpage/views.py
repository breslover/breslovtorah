'''
Created on Nov 2, 2014

@author: coderam
'''

import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse
from django.template import loader, Context

# models
from breslovtorah.shiur.models import Shiur

def home(request):
    
    # grab the top element in the Shiur table
    try:
        daily_shiur = Shiur.objects.filter().order_by('-id')[0]
    except:
        daily_shiur = None
        logger.exception('Could not find shiur!')
    
    # load the template
    t = loader.get_template('base.html')
    c = Context({ 'daily_shiur': daily_shiur })
    return HttpResponse(t.render(c)) # content_type="application/xhtml+xml"
