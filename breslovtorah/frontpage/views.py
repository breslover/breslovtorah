'''
Created on Nov 2, 2014

@author: coderam
'''

import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# models
from breslovtorah.shiur.models import Shiur, Sefer

def home(request):
    
    # grab the top element in the Shiur table
    try:
        daily_shiur = Shiur.objects.filter(type=Shiur.TYPES_SHORTDAILY).order_by('-id')[0]
    except:
        daily_shiur = None
        
    # grab the list of sefarim from the Sefer table
    sefers_maimon = Sefer.objects.filter(user__username='maimon')
    sefers_rosenfeld = Sefer.objects.filter(user__username='rosenfeld')
    sefers_arvi = Sefer.objects.filter(user__username='arvi')    
    # load the template
    t = loader.get_template('base.html')
    c = Context({ 'request': request, 'daily_shiur': daily_shiur, 'sefers_maimon': sefers_maimon, 'sefers_rosenfeld': sefers_rosenfeld, 'sefers_arvi': sefers_arvi })

    return HttpResponse(t.render(c)) # content_type="application/xhtml+xml"
    #return HttpResponseRedirect('http://breslev.co.il')
def sefer(request, slug=None):
    
    page = request.GET.get('page', None)
    
    # grab the list of sefarim from the Sefer table
    sefer = Sefer.objects.get(slug=slug)
    
    if sefer.sort_descending:
        shiurs = Shiur.objects.filter(sefer__slug=slug).order_by('-id')
    else:
        shiurs = Shiur.objects.filter(sefer__slug=slug)
        
    paginator = Paginator(shiurs, 25) # Show 25 contacts per page
    
    try:
        shiurim = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        shiurim = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        shiurim = paginator.page(paginator.num_pages)
    
    # load the template
    t = loader.get_template('base_sefer.html')
    c = Context({ 'request': request, 'shiurim': shiurim, 'sefer': sefer })
    return HttpResponse(t.render(c)) # content_type="application/xhtml+xml"
