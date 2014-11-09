from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# ordered_model
from ordered_model.models import OrderedModel

class Sefer(OrderedModel):
    
    user = models.ForeignKey(User, null=True, blank=True)
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    
    class Meta(OrderedModel.Meta):
        pass
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.slug = slugify(self.title)
        return super(Sefer, self).save(*args, **kwargs)
    
class Shiur(OrderedModel):
    
    TYPES_DAILYSHIUR =  'DAILY'
    TYPES_WEEKLYSHIUR = 'WEEKL'
    TYPES_SHORTDAILY =  'SHORT'
    
    TYPES = (
        (TYPES_DAILYSHIUR, u'Daily shiur'),
        (TYPES_WEEKLYSHIUR, u'Weekly shiur'),
        (TYPES_SHORTDAILY, u'Video clip of the day!'),
    )
    
    type = models.CharField(max_length=5, choices=TYPES)
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    video_url = models.URLField(null=True, blank=True)
    mp3_url = models.URLField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, blank=True)
    sefer = models.ForeignKey(Sefer, null=True, blank=True)
    
    class Meta(OrderedModel.Meta):
        pass
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.slug = slugify(self.title)
        return super(Shiur, self).save(*args, **kwargs)


