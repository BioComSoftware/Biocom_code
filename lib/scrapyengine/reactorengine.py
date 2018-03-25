from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from test.spiders.auctiondotcom import AuctionDOTcom
# from testspiders.spiders.followall import FollowAllSpider
from scrapy.utils.project import get_project_settings

class ReactorEngine:
    def __init__(self):
        spider = AuctionDOTcom(domain='auction.com')
        # spider = FollowAllSpider(domain='scrapinghub.com')
        # spider = FollowAllSpider(domain='www.auction.com/')
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
        # log.start()
        reactor.run() # the script will block here until the spider_closed signal was sent

if __name__ == "__main__":
    r = ReactorEngine(name = "auction.com", 
                      allowed_domains = ["auction.com"], 
                      start_urls = ('http://www.auction.com/search',))