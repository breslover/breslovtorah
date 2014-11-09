#-*- coding: UTF-8 -*-
# http://blog.miguelgrinberg.com/post/easy-web-scraping-with-python
import urllib2
import bs4

# django 
from django.core.management.base import BaseCommand, CommandError, make_option
from django.contrib.auth.models import User

# models
from breslovtorah.shiur.models import Shiur, Sefer

class Command(BaseCommand):
    help = 'Scrape BreslovTorah.com or BreslovTorah.net for a list of shiurs and also the daily shiur'
    option_list = BaseCommand.option_list + (
        make_option('--frontpage',
            action='store_true',
            dest='frontpage',
            help='Scrape the front-page for the daily video, etc.'),
        make_option('--mp3',
            action='store_true',
            dest='mp3',
            help='Scrape the different categories on the left hand side of breslovtorah.com and add to the db, etc.'),
    )
        
    def handle(self, *args, **options):
        
        if 'mp3' in options and options['mp3']:
            self.stdout.write('mp3... start')
            response = urllib2.urlopen('http://www.breslovtorah.com/')
            soup = bs4.BeautifulSoup(response)
            sefer_links = soup.select('div.execphpwidget ul li a')
            for link in sefer_links:
                href = link.attrs.get('href')
                title_innerhtml = link.decode_contents(formatter="html")
                title_innerhtml = title_innerhtml.strip()
                self.stdout.write('link: %s' % href)
                self.stdout.write('title_innerhtml: %s' % title_innerhtml)
                self.stdout.write('-----------------------')
                
                try:
                    sefer = Sefer.objects.filter(title=title_innerhtml)[0]
                    self.stdout.write('found sefer by title, not saving...')
                except:
                    sefer = Sefer()
                    sefer.user = User.objects.get(username='maimon')
                    sefer.title = title_innerhtml
                    sefer.save()
                    self.stdout.write('saved sefer by title...')
                    
                # open up each page!
                response = urllib2.urlopen(href)
                soup = bs4.BeautifulSoup(response)
                shiur_titles_mp3 = soup.select('div#content li p')
                shiur_titles_mp3 = iter(shiur_titles_mp3)
                for t_mp3 in shiur_titles_mp3:
                    object = t_mp3.findNext('object')
                    self.stdout.write('object: %s' % object)
                    try:
                        object_mp3 = object.select('param[name="FlashVars"]')[0]['value']
                        object_mp3 = object_mp3.replace('mp3=', '').replace('&showvolume=1','')
                    except:
                        next(shiur_titles_mp3, None)
                        
                    self.stdout.write('object_mp3: %s' % object_mp3)
                    title = t_mp3.a.decode_contents(formatter="html")
                    self.stdout.write('title: %s' % title)
                    self.stdout.write('--------')
                    
                    # save to db
                    try:
                        shiur = Shiur.objects.filter(title=title, sefer=sefer)[0]
                        self.stdout.write('found shiur by title, not saving...')
                    except:
                        shiur = Shiur()
                        shiur.type = Shiur.TYPES_DAILYSHIUR
                        shiur.title = title
                        shiur.mp3_url = object_mp3
                        shiur.sefer = sefer
                        shiur.user = User.objects.get(username='maimon')
                        shiur.save()
                        self.stdout.write('saving shiur...')
                        
            self.stdout.write('mp3... stop')
            
        if 'frontpage' in options and options['frontpage']:
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
            
