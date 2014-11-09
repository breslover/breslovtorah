'''
Created on Nov 2, 2014

@author: coderam
'''

import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse
from django.template import loader, Context
from django.contrib.auth.models import User


# models
from breslovtorah.shiur.models import Shiur, Sefer

def home(request):
    
    # grab the top element in the Shiur table
    try:
        daily_shiur = Shiur.objects.filter(type=Shiur.TYPES_SHORTDAILY).order_by('-id')[0]
    except:
        daily_shiur = None
        
    # grab the list of sefarim from the Sefer table
    sefers_maimon = Sefer.objects.filter(user=User.objects.get(username='maimon'))
    
    # load the template
    t = loader.get_template('base.html')
    c = Context({ 'daily_shiur': daily_shiur, 'sefers_maimon': sefers_maimon })
    return HttpResponse(t.render(c)) # content_type="application/xhtml+xml"
