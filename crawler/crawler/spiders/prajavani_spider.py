__author__ = 'swvenu'

from scrapy.spiders import Rule, CrawlSpider
from crawler.items import CrawlerItem
from urlparse import urlparse
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import scrapy

class MySpider(CrawlSpider):
    name = "prajavani"
    allowed_domains = ["prajavani.net"]
    start_urls = [ "http://www.prajavani.net/categories/%E0%B2%95%E0%B3%8D%E0%B2%B0%E0%B3%80%E0%B2%A1%E0%B3%86-0"]
    rules = (

        Rule(
            LxmlLinkExtractor(restrict_xpaths=("//div[contains(@class,'view-display-id-page')]",)),
            callback='parse_article',
            follow=True

        ),

    )

    def parse_article(self, response):
        main = response.xpath('//div[@class="main-content clearfix"]')
        title = main.xpath('//h1[@id="page-title"]/text()').extract()
        content = main.xpath('//div[@class="field-item even"]/p').extract()
        item = CrawlerItem()
        if len(content) == 0:
            return
        item["url"] = response.url
        item["content"] = []
        c = ""
        for i in range(0,len(content)):
            if i == 0:
                continue
            if i == 1:
                c = content[0] + content[1]
            else:
                c = content[i]

            if c == "*****":
                break
            if len(c) > 3:
                c = c.replace('\t','').replace('<br>','').replace('<p>','').replace('</p>','').replace('<strong>','').replace('</strong>','').replace('\n','')
                item["content"].append(c)


            item["title"] = title[0].replace('<', '').replace('>', '').replace(':', '').replace('"', '').replace('/', '').replace('|', '').replace('*', '').replace('?', '')
#        with open("crawled/"+title+".html", 'wb') as f:
#            f.write(response.body)
        return item