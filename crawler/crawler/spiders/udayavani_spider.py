__author__ = 'swvenu'

from scrapy.spiders import Rule, CrawlSpider
from crawler.items import CrawlerItem
from urlparse import urlparse
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import scrapy

class MySpider(CrawlSpider):
    name = "udayavani"
    allowed_domains = ["udayavani.com"]
    start_urls = [ "http://www.udayavani.com/kannada/category/sports-news"]
    rules = (

        Rule(
            LxmlLinkExtractor(restrict_xpaths=("//div[@id='block-system-main']",)),
            callback='parse_article',
            process_links='link_filtering',
            follow=True

        ),

    )

    def parse_article(self, response):
        main = response.xpath('//div[@id="main-content"]')
        title = main.xpath('//h1[@id="page-title"]/span/text()').extract()
        content = main.xpath('//div[@class="field field-name-body field-type-text-with-summary field-label-hidden"]/div/div/node()').extract()
        item = CrawlerItem()
        if len(content) == 0:
            return
        item["url"] = response.url
        item["title"] = title[0]
        item["content"] = []

        for c in content:
            if len(c) > 1:
                c = c.replace('<br>','').replace('<p>','').replace('</p>','').replace('<strong>','').replace('</strong>','').replace('\n','')
                item["content"].append(c)


        title = title[0].replace('<', '').replace('>', '').replace(':', '').replace('"', '').replace('/', '').replace('|', '').replace('*', '').replace('?', '')
        with open("crawled/"+title+".html", 'wb') as f:
            f.write(response.body)
        return item

    def link_filtering(self, links):
        ret = []
        for link in links:
            if "kannada" in link.url:
                ret.append(link)
        return ret