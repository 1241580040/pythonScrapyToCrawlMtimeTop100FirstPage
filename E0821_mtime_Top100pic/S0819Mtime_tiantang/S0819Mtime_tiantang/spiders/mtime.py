# -*- coding: utf-8 -*-
import scrapy
import random
from S0819Mtime_tiantang.items import S0819MtimeTiantangItem
import re
from Carbon.Files import fHasBundle

class MtimeSpider(scrapy.Spider):
    name = "mtime"
    allowed_domains = ["http://www.mtime.com"]
    start_urls = (
        'http://www.mtime.com/top/movie/top100',
    )

    def parse(self, response):
        #print response
        #allpics = response.xpath("//script[@type='text/javascript']").extract()[4]
        
        allMovieWebsite = response.xpath("//div/ul[@id='asyncRatingRegion']/li//h2/a/@href").extract()
        print allMovieWebsite
        
        for oneMovieWebsite in allMovieWebsite:
            oneMovieAllPicWebSite = oneMovieWebsite+"posters_and_images/"
            print oneMovieAllPicWebSite
            request = scrapy.Request(oneMovieAllPicWebSite, callback=self.parse_item, dont_filter=True)
            print request
            yield request
        
    def parse_item(self, response):
        print "aaaa"
        allpics = response.xpath("//script[@type='text/javascript']").re('\"img_1000\":\"(.+?jpg)\"')
        #picName = response.xpath("//title").extract()[0]
        picName = response.xpath("/html/body/div[@id='db_sechead']/div[@class='db_head']/div[@class='clearfix']/h1/a").extract()[0]
        regexName = re.compile(">(.+?)<")
        picName = regexName.findall(picName)[0].encode("utf8")
        print picName
        picCount = len(allpics)
        print picCount
        
        with open("./"+picName+"_"+str(picCount)+".txt", "w") as fh:
            for picWebSite in allpics:
                fh.write(picWebSite+"\n")
        
        i = 0
        for pic in allpics:
            i = i+1
            item = S0819MtimeTiantangItem()
            addr = pic 
            item['name'] = picName+"_"+str(i)
            item['picCount'] = picCount
            item['addr'] = addr
            print "+++++"+item['addr']
            print "+++++"+item['name']
            yield item
            
