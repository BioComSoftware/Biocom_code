from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from estatescraper.spiders.openspider import OpenSpider
# from testspiders.spiders.followall import FollowAllSpider
from scrapy.utils.project import get_project_settings

class SpiderRun:
    def __init__(self, name, allowed_domains, start_urls):
#         spider = OpenSpider(domain='auction.com')
        spider = OpenSpider(name, allowed_domains, start_urls)
        # spider = FollowAllSpider(domain='scrapinghub.com')
        # spider = FollowAllSpider(domain='www.auction.com/')
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
#         log.start()
        reactor.run() # the script will block here until the spider_closed signal was sent
        self.cleanup()
        
    def cleanup(self):
        print "SpiderRun done"
        
if __name__ == "__main__":
    r = SpiderRun(name = "auction.com", 
                      allowed_domains = ["auction.com"], 
                      start_urls = ('http://www.auction.com/search',))