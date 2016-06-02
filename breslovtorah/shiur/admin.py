'''
Created on Nov 9, 2014

@author: coderam
'''

from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from models import Shiur, Sefer

class ShiurAdmin(OrderedModelAdmin):
    list_display = ('title', 'move_up_down_links')
    list_filter = ('sefer__title',)
    exclude = ('slug',)
    
admin.site.register(Shiur, ShiurAdmin)

class SeferAdmin(OrderedModelAdmin):
    list_display = ('title', 'move_up_down_links')
    exclude = ('slug',)

admin.site.register(Sefer, SeferAdmin)
