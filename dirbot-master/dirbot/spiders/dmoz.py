from scrapy.spider import Spider
from scrapy.selector import Selector

from dirbot.items import Stock

from scrapy.http import Request
from scrapy.mail import MailSender



class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["xueqiu.com"]
    start_urls = [
        "http://xueqiu.com/P/ZH010389",
    ]
    #def start_requests(self):        
        #yield Request("http://xueqiu.com/P/ZH010389",  
                  #headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
                           #Chrome/39.0.2171.71 Safari/537.36"})
    # override method
    def make_requests_from_url(self, url):
        request = Request(url, dont_filter=True,
                          headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
                           #Chrome/39.0.2171.71 Safari/537.36"})
        # set the meta['start_url'] to use the item in the next call back
        request.meta['start_url'] = url
        return request

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        sel = Selector(response)
        stocks = sel.xpath('//a[@class="stock fn-clear no-tooltip"]')
        items = []
        content = ''
        for stock in stocks:
            item = Stock()
            item['start_url'] = response.meta['start_url']
            item['name'] = stock.xpath('span[@class="stock-name"]/text()').extract()
            item['weight'] = stock.xpath('span[@class="stock-weight weight"]/text()').extract()
            content += item['name'][0]+' '+item['weight'][0]+' '
            items.append(item)
        #TODO: replace this hard-code file name by url relevant
        fo = open("F:/trading/dirbot-master/positions.txt",'r')
        oldcontent=fo.read().decode('UTF-8')
        fo.close()
        if content != oldcontent:
            mailer = MailSender(mailfrom="kasajqbot@gmail.com",smtphost="smtp.gmail.com",smtpport=587,
                        smtpuser="kasajqbot@gmail.com",smtppass="12346789jq")
            mailer.send(to=["kasajq@gmail.com"],
                        subject="[AutoMail]Position Changed",
                        body="Portfolio Link on Xueqiu: " + item['start_url']+"\n"
                        +"New positon: "+content.encode('UTF-8')+"\n"
                        +"Previous position: "+oldcontent.encode('UTF-8')+"\n"
                        
                        ) 
            #mailer.send(to=["kasajq@gmail.com","yingyj08@gmail.com ","ylz123@126.com"],
            #            subject="[AutoMail]Position Changed",body=content.encode('UTF-8'))        
            fo = open("F:/trading/dirbot-master/positions.txt",'w')
            fo.write(content.encode('UTF-8'))
            fo.close()
        return items
