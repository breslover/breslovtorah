'''
Created on Nov 2, 2014

@author: coderam
'''

from django.http import HttpResponse
from django.template import loader, Context

def home(request):
    t = loader.get_template('base.html')
    c = Context({  })
    return HttpResponse(t.render(c)) # content_type="application/xhtml+xml"