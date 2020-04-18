# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

#a spider with different template than the defaut(the crawl template spider)
class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['www.imdb.com']
    # start_urls = ['https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc']
    
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/81.0.4044.92 Chrome/81.0.4044.92 Safari/537.36'
    # In crawlSpider when we ovverride the static request mehtod(start_requests mehtod) we don't have to specify the callback property unlike the default template
    def start_requests(self):
        yield scrapy.Request(url = 'https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc',headers={
            'User-Agent' : self.user_agent
        })


    #the rules is a python tuple(it's a datastructure w/c immutable(the data inside is unchangable))
    rules = (
        #the rule object is used to tell the crawl spider what r the link u want to follow regarding the web we are scrapping
        # "follow" tells the rule object whether u want to open or send a request to link extracted or not
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"),process_request='set_user_agent')
    )
    def set_user_agent(self,request):
        request.headers['User-Agent'] = self.user_agent,
        return request


    def parse_item(self, response):
      yield{
            'title': response.xpath("//div[@class='title_wrapper']/h1/text()").get(),
            'year': response.xpath("//span[@id='titleYear']/a/text()").get(),
            #normalize-space removes the white space charactcters from the returned data
            'duration': response.xpath("normalize-space((//time)[1]/text())").get(),
            'genre': response.xpath("//div[@class='subtext']/a[1]/text()").get(),
            'rating': response.xpath("//span[@itemprop='ratingValue']/text()").get(),
            'movie_url': response.url,
            # 'user-agent':response.request.headers['User-Agent']


      }
