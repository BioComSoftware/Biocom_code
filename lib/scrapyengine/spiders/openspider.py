from scrapy.spider import Spider
# from testspiders.items import Page as HomehoundItem #333
from scrapy.selector import Selector
from scrapy.http import Request

import urlparse
import time 

class OpenSpider(Spider):
    """"""
    def __init__(self, name, allowed_domains, start_urls):
        self.name = name
        self.allowed_domains = allowed_domains
        self.start_urls = start_urls
        
#         self.name = "auction.com"
#         self.allowed_domains = ["auction.com"]
#         self.start_urls = (
#             'http://www.auction.com/search',
#             )

    def parse(self, response):
        self.response = response
        self.parse_test()
#         return response
#         sel = Selector(response)
#         listings=  sel.xpath('//input[@type="checkbox"]').extract()
# #         print response.body() #333
# #         listings = sel.xpath('//div[@type="checkbox"]').extract()
#         for i in listings: #333
#             print i #333
#         
#         listings = sel.xpath('//a[@class="detailsButton button"]//@href').extract()
#         for property_link in listings:
#             item = HomehoundItem()
#             print "property_link = ", property_link #333
#             if '/rent' in response.url:
#                 item['listing_type'] = 'rent'
#             elif '/buy' in response.url:
#                 item['listing_type'] = 'buy'
#             yield Request("http://%s/%s" % (urlparse.urlparse(response.url).hostname, property_link), meta = { 'item' : item } , callback=self.parse_listing)
        
#         next = set(sel.xpath('//a[contains(text(),"Next")]//@href').extract())
#         for i in next:
#             yield Request("http://%s/%s" % (urlparse.urlparse(response.url).hostname, i), callback=self.parse)

    def parse_test(self):
        sel = Selector(self.response)
        item = self.response.meta['item']
        for i in item:
            print i
#         listings=  sel.xpath('//input[@type="checkbox"]').extract()
# #         print response.body() #333
# #         listings = sel.xpath('//div[@type="checkbox"]').extract()
#         for i in listings: #333
#             print i #333
# #     def parse_listing(self, response):
#         sel = Selector(response)
#         item = response.meta['item']
#         
#         item['modTime'] = time.strftime('%Y-%m-%d-%H:%M:%S')
#         item['status'] = 'current'
#         item['uniqueID'] = ''.join(set(sel.xpath('//span[@class="property_id"]//text()').extract())).replace('Property No.','').strip()
#         item['agent_name'] = ''.join(set(sel.xpath('//p[@class="agentName"]/strong/text()').extract()))
#         item['agent_telephone'] = ''.join(set(sel.xpath('//a[@rel="showContact"]/@data-value').extract()))
#         item['priceView'] = ''.join(sel.xpath('//ul//p/span[@class="hidden"]//text()').extract())
#         item['price'] = ''.join(sel.xpath('//ul//p/span[@class="hidden"]//text()').re('\d+'))
#         
#         item['address'] = 'yes'
#         try:
#             item['streetNumber'] = ''.join(sel.xpath('//span[@itemprop="streetAddress"]//text()').extract()).split()[0].strip()
#         except:
#             item['streetNumber'] = ''
#         item['street'] = ''.join(sel.xpath('//span[@itemprop="streetAddress"]//text()').extract()).replace(item['streetNumber'] ,'').strip()
#         item['suburb'] = ''.join(sel.xpath('//span[@itemprop="addressLocality"]//text()').extract())
#         item['state'] = ''.join(sel.xpath('//span[@itemprop="addressRegion"]//text()').extract()).lower()
#         item['postcode'] = ''.join(sel.xpath('//span[@itemprop="postalCode"]//text()').extract())
#         item['country'] = 'AUS'
#         item['category'] = ''.join(sel.xpath('//span[@class="propertyType"]//text()').extract())
#         item['headline'] = ''.join(sel.xpath('//p[@class="title"]//text()').extract())
#         item['description'] = '\n'.join(sel.xpath('//p[@class="body"]//text()').extract())
#         item['bedrooms'] = ''.join(sel.xpath('//li[contains(text(),"Bedrooms")]//span//text()').extract())
#         item['bathrooms'] = ''.join(sel.xpath('//li[contains(text(),"Bathrooms")]//span//text()').extract())
#         item['garages'] = ''.join(sel.xpath('//li[contains(text(),"Garage Spaces")]//span//text()').extract())
#         item['carports'] = ''.join(sel.xpath('//li[contains(text(),"Carport Spaces")]//span//text()').extract())
#         features = sel.xpath('//div[@id="features"]//text()').extract()
#         if 'Air Conditioning' in features:
#             item['airConditioning'] = 'yes'
#         if 'Balcony' in features:
#             item['balcony'] = 'yes'
#         if 'Outdoor Entertaining' in features:
#             item['outdoorEnt'] = 'yes'
#         item['otherFeatures'] = ''.join(sel.xpath('//li[preceding-sibling::li[contains(text(),"Other Features")]]//text()').extract())
#         tmp_inspectionTimes = sel.xpath('//a[@itemprop="events"]/span[@class="time"]/text()').extract()
#         tmp_inspectionDates = sel.xpath('//a[@itemprop="events"]/strong[@itemprop="name"]/text()').extract()
# 
#         item['inspectionTimes'] = [i+'  '+j for i,j in zip(tmp_inspectionDates,tmp_inspectionTimes)]
#         item['vendor_name'] = 'Avenue One Property Group'
#         item['vendor_telephone'] = '9228 4616'
#         item['externalLink'] = response.url
#         tmp_imgs = sel.xpath('//img[contains(@class,"thumb_")]/@src').extract()
#         item['images'] = []
#         for id,img in enumerate(tmp_imgs):
#             tmp_img = {}
#             tmp_img['id'] = str(id)
#             tmp_img['modTime'] =time.strftime("%Y-%m-%d-%H:%M:%S")
#             tmp_img['url'] = img.replace('120x90','10000x10000')
#             tmp_img['format'] = 'jpg'
#             item['images'].append(tmp_img)
# 
#         return item 