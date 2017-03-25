# -*-coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.utils.response import get_base_url
from recruit.items import RecruitItem
from scrapy_splash import SplashRequest
import time
import random


class TanYanTongSpider(CrawlSpider):
    name = 'TianYanTong'
    allow_domains = ['tianyancha.com']
    start_urls = ['http://www.tianyancha.com/search/p{}'.format(page) for page in xrange(1, 51)]

    proxies = {
        'http1': 'http://117.175.183.10:84',
        'http2': 'http://117.63.50.213:8998',
        'http3': 'http://183.141.154.66:3128',
        'http4': 'http://117.22.71.109:8998',
        'http5': 'http://121.232.146.248:9000',
    }

    def start_requests(self):
        page = 0
        time_dalay = random.randint(1, 3)

        for url in self.start_urls:
            page += 1
            headers = {'Accept': 'application/json, text/plain, */*',
                        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
                        'Cookie': 'aliyungf_tc=AQAAALx/yhBBjgIArZFJdTgpPylQTJYb; TYCID=5b416d7278c94378875393943f6f5872; RTYCID=a93badb0127d48f7b3c74619fe561208; _pk_ref.1.e431=%5B%22%22%2C%22%22%2C1489963230%2C%22http%3A%2F%2Fantirobot.tianyancha.com%2Fcaptcha%2Fverify%3Freturn_url%3Dhttp%3A%2F%2Fwww.tianyancha.com%2Fcompany%2F375943060%26rnd%3DfUX-kfDb0aixV-Q5FGbxmQ%3D%3D%22%5D; tnet=117.73.145.220; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1489909651,1489928653,1489964059,1489968907; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1489968929; _pk_id.1.e431=d7a82980505f9f5e.1489562827.16.1489968930.1489963230.; _pk_ses.1.e431=*; token=39dd0ca635114a5b9bee71e9aa444213; _utm=2rr982dd3-9--82htt9n44v-dthd9-rd; paaptp=f4115d4ce07b4ed75be3a39b1cde4389465242064704c81f0b15ae911d7dc',
                        'Host': 'www.tianyancha.com',
                        'Referer': 'http://www.tianyancha.com/search/p{}'.format(page-1),
                        'User-Agent': "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
                        'X-Requested-With': 'XMLHttpRequest',
                    }
            splash_args = {
                'wait': time_dalay,
                "http_method": "GET",
                "render_all": 1,
                "headers": headers,
                "proxies": self.proxies,
            }
            if page in list(range(1, 51, 10)):
                time.sleep(3)
            yield SplashRequest(url,
                                self.parse,
                                args=splash_args,
                                )

    def parse(self, response):
        time_dalay = random.randint(1, 3)
        splash_args = {
            'wait': time_dalay,
            "http_method": "GET",
            "proxies": self.proxies,
        }
        for link in LinkExtractor(allow=('company/\d+')).extract_links(response):
            yield SplashRequest(link.url,
                                self.parse_item,
                                args=splash_args,
                                )

    def parse_item(self, response):
        sel = Selector(response)
        base_url = get_base_url(response)
        item = RecruitItem()
        time_dalay = random.randint(1, 3)

        splash_args = {
            'wait': time_dalay,
            "http_method": "GET",
            "proxies": self.proxies,
        }

        try:
            item['enterpreneur_name'] = sel.xpath('//div[@class="baseinfo-module-content-value-fr baseinfo-module-content-value"]/a/@title').extract()[0]
            item['company_name'] = sel.xpath('//div[@class="in-block ml10 f18 mb5 ng-binding"]/text()').extract()[0]
            item['company_addr'] = sel.xpath('//*[@id="ng-view"]/div[2]/div/div/div/div[1]/div/div[6]/table/tbody/tr[5]/td/div/span/text()').extract()[0]
            return item
        except:
            time.sleep(time_dalay)
            yield SplashRequest(base_url,
                                self.parse_item,
                                args=splash_args,
                                )
            # 传入给piplelines的 到底是什么。biubiu
            # request里的args里的proxies如何切换的，是否真的可以切换。
            '''
            一般是 筛选完成后，得到可用的ip列表，然后可以从里面按照调用的时间等参数，进行选择。
            '''
            # 最后这个yeild我认为是有问题的。如果ip有问题的话，那么就一直会循环.话说用return一样的吧，又没有for
            # scrapy是否有切换代理的机制
            '''
            切换机制一般自己定义。
            可以 写在middleware里。
            详细的midderware在setting设置产生的效果有待查证。
            '''
            # scrapy的轮训机制到底是怎样的
            '''
            例如 有大量的链接，先从start_request里面获取链接啦，然后再处理呗
            start_request是有限的啦。哎。根据具体的定义而不同。
            记得直接获取了很多的页面的链接的时候，记得set去重。
            '''
            # user_agent一大串如何切换
            '''
            可以用random.choice随便选一个啦，保证一大串都是可用的就好了。每次发送请求的时候，都随便切换一个。
            '''