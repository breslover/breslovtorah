from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

    
class Shiur(models.Model):
    
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
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.slug = slugify(self.title)
        return super(Shiur, self).save(*args, **kwargs)


