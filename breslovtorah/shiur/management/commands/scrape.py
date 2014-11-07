# http://blog.miguelgrinberg.com/post/easy-web-scraping-with-python
import urllib2
import bs4

# django 
from django.core.management.base import BaseCommand, CommandError, make_option
from django.contrib.auth.models import User

# models
from breslovtorah.shiur.models import Shiur

class Command(BaseCommand):
    help = 'Scrape BreslovTorah.com or BreslovTorah.net for a list of shiurs and also the daily shiur'
    option_list = BaseCommand.option_list + (
        make_option('--frontpage',
            action='store_true',
            dest='frontpage',
            help='Scrape the front-page for the daily video, etc.'),
    )
        
    def handle(self, *args, **options):
        
        if 'frontpage' in options:
            self.stdout.write('frontpage... start')
            response = urllib2.urlopen('http://www.breslovtorah.com/')
            soup = bs4.BeautifulSoup(response)
            video_iframe = soup.select('iframe#player_1')[0]
            video_iframe_src = video_iframe.attrs.get('src')
            self.stdout.write('frontpage... video_iframe_src: %s' % video_iframe_src)
            video_title = soup.select('div.backgrounds div.item h2')[0]
            video_title_innerhtml = video_title.decode_contents(formatter="html")
            video_title_innerhtml = video_title_innerhtml.strip()
            self.stdout.write('frontpage... video_title_innerhtml: %s' % video_title_innerhtml)
            
            # save to db
            try:
                shiur = Shiur.objects.filter(title=video_title_innerhtml)[0]
            except:
                shiur = Shiur()
                shiur.type = Shiur.TYPES_DAILYSHIUR
                shiur.title = video_title_innerhtml
                shiur.video_url = video_iframe_src
                shiur.user = User.objects.get(username='maimon')
                shiur.save()
                self.stdout.write('frontpage... saved shiur object: %s' % shiur)
                
            self.stdout.write('frontpage... stop')
            
        self.stdout.write('Successfully scraped BreslovTorah poll')