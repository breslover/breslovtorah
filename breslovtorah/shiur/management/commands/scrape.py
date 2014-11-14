#-*- coding: UTF-8 -*-
# http://blog.miguelgrinberg.com/post/easy-web-scraping-with-python
import urllib2
import bs4

# django 
from django.core.management.base import BaseCommand, make_option #CommandError
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
        make_option('--pagination',
            action='store_true',
            dest='pagination',
            help='Scrape the different categories on the left and visit the pages in each category/sefer.'),
        make_option('--video',
            action='store_true',
            dest='video',
            help='Scrape the different videos from each category.'),
    
    )
    
    def handle(self, *args, **options):
        
        if 'video' in options and options['video']:
            self.stdout.write('video... start')
            shiurs_no_mp3 = Shiur.objects.filter(mp3_url=None).filter(video_url=None)
            for shiur in shiurs_no_mp3:
                self.stdout.write('shiur: %s' % shiur)
                if shiur.wp_url:
                    response = urllib2.urlopen(shiur.wp_url)
                    soup = bs4.BeautifulSoup(response)
                    iframe = soup.select('div#content iframe')[0]
                    iframe_src = iframe.attrs.get('src', None)
                    if iframe_src:
                        self.stdout.write('iframe_src: %s' % iframe_src)
                        shiur.video_url = iframe_src
                        shiur.save()
                        self.stdout.write('iframe_src saved!')
                        self.stdout.write('----------------------')
                        
            self.stdout.write('video... stop')
        
        if 'mp3' in options and options['mp3']:
            self.stdout.write('mp3... start')
            response = urllib2.urlopen('http://www.breslovtorah.com/')
            soup = bs4.BeautifulSoup(response, 'html.parser')
            sefer_links = soup.select('div.execphpwidget ul li a')
            for link in sefer_links:
                href = link.attrs.get('href')
                title_innerhtml = link.decode_contents(formatter="html")
                title_innerhtml = title_innerhtml.strip()
                self.stdout.write('link: %s' % href)
                self.stdout.write('title_innerhtml: %s' % title_innerhtml)
                self.stdout.write('-----------------------')
                
                try:
                    sefer = Sefer.objects.filter(title=title_innerhtml.strip())[0]
                    self.stdout.write('found sefer by title, not saving...')
                except:
                    sefer = Sefer()
                    sefer.user = User.objects.get(username='maimon')
                    sefer.title = title_innerhtml.strip()
                    sefer.title_friendly = title_innerhtml.strip()
                    sefer.save()
                    self.stdout.write('saved sefer by title...')
                    
                # open up each page!
                response = urllib2.urlopen(href)
                soup = bs4.BeautifulSoup(response)
                shiur_titles_mp3 = soup.select('div#content li p')
                shiur_titles_mp3 = iter(shiur_titles_mp3)
                for t_mp3 in shiur_titles_mp3:
                    object_mp3 = None
                    object = t_mp3.findNext('object')
                    self.stdout.write('object: %s' % object)
                    try:
                        object_mp3 = object.select('param[name="FlashVars"]')[0]['value']
                        object_mp3 = object_mp3.replace('mp3=', '').replace('&showvolume=1','')
                    except:
                        self.stdout.write('object_mp3 = None')
                        #next(shiur_titles_mp3, None)
                        object_mp3 = None
                        
                    self.stdout.write('object_mp3: %s' % object_mp3)
                    title = t_mp3.a.decode_contents(formatter="html")
                    wp_href = t_mp3.a.attrs.get('href', None)
                    self.stdout.write('title: %s' % title)
                    self.stdout.write('wp_href: %s' % wp_href)
                    self.stdout.write('--------')
                    
                    # save to db
                    try:
                        shiur = Shiur.objects.filter(title=title.strip(), sefer=sefer)[0]
                        self.stdout.write('found shiur by title, not saving...')
                    except:
                        shiur = Shiur()
                        shiur.type = Shiur.TYPES_DAILYSHIUR
                        shiur.title = title.strip()
                        shiur.wp_url = wp_href
                        shiur.mp3_url = object_mp3
                        shiur.sefer = sefer
                        shiur.user = User.objects.get(username='maimon')
                        try:
                            shiur.save()
                            self.stdout.write('saving shiur...')
                        except:
                            self.stdout.write('failed saving shiur... not unique')

                # handle the page #s
                if 'pagination' in options and options['pagination']:
                    # the new pagination code for extracting page #s
                    try:
                        pages_string = soup.select('div.wp-pagenavi span.pages')[0]
                        pages_string = pages_string.decode_contents(formatter="html").strip()
                        self.stdout.write('pages_string: %s' % pages_string)
                        pages_string = pages_string.replace('Page 1 of ', '')
                        pages_int = int(pages_string)
                        self.stdout.write('pages_int: %s' % pages_int)
                        self.stdout.write('href: %s' % href)
                    except:
                        pages_int = 0
                        self.stdout.write('there is no pagination on: %s' % href)
                        
                    for page_number in range(1, pages_int+1):
                        self.stdout.write('------------------')
                        self.stdout.write('------------------')
                        self.stdout.write('------------------')
                        self.stdout.write('------------------')
                        self.stdout.write('------------------')
                        
                        href_page = '%s/page/%s/' % (href, page_number)
                        self.stdout.write('href_page: %s' % href_page)
                        response = urllib2.urlopen(href_page)
                        
                        soup = bs4.BeautifulSoup(response, 'html.parser')
                        #soup3 = BeautifulSoup(response)
                        #from pyquery import PyQuery as pq
                        #d = pq(response)
                        
                        shiur_titles_mp3 = soup.select('div#content li p')
                        shiur_titles_mp3 = iter(shiur_titles_mp3)
                        for t_mp3 in shiur_titles_mp3:
                            object_mp3 = None
                            object = t_mp3.findNext('object')
                            self.stdout.write('object: %s' % object)
                            try:
                                object_mp3 = object.select('param[name="FlashVars"]')[0]['value']
                                object_mp3 = object_mp3.replace('mp3=', '').replace('&showvolume=1','')
                            except:
                                self.stdout.write('object_mp3 = None')
                                #next(shiur_titles_mp3, None)
                                object_mp3 = None
                                
                            self.stdout.write('object_mp3: %s' % object_mp3)
                            title = t_mp3.a.decode_contents(formatter="html")
                            wp_href = t_mp3.a.attrs.get('href', None)
                            self.stdout.write('title: %s' % title)
                            self.stdout.write('wp_href: %s' % wp_href)
                            self.stdout.write('--------')
                            
                            # save to db
                            try:
                                shiur = Shiur.objects.filter(title=title.strip(), sefer=sefer)[0]
                                self.stdout.write('found shiur by title, not saving...')
                            except:
                                shiur = Shiur()
                                shiur.type = Shiur.TYPES_DAILYSHIUR
                                shiur.title = title.strip()
                                shiur.wp_url = wp_href
                                shiur.mp3_url = object_mp3
                                shiur.sefer = sefer
                                shiur.user = User.objects.get(username='maimon')
                                try:
                                    shiur.save()
                                    self.stdout.write('saving shiur...')
                                except:
                                    self.stdout.write('failed saving shiur from pagination')
                                    
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
                shiur.type = Shiur.TYPES_SHORTDAILY
                shiur.title = video_title_innerhtml
                shiur.video_url = video_iframe_src
                shiur.user = User.objects.get(username='maimon')
                shiur.save()
                self.stdout.write('frontpage... saved shiur object: %s' % shiur)
                
            self.stdout.write('frontpage... stop')
            
