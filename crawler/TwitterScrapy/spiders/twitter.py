# -*- coding: utf-8 -*-

import json
import logging
from urllib.parse import quote
from datetime import datetime

from scrapy import http
from scrapy.utils.project import get_project_settings
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider

from TwitterScrapy.items import TwitterItem

settings = get_project_settings()

logger = logging.getLogger(__name__)

class TwitterScrapy(CrawlSpider):
    """ 
        Classe responsavel por capturar os dados(posts e comentarios) dos tweets.
        O twitter disponibiliza algumas formas de pesquisas avancadas, e foi adota para
        este projeto tais metodos:

        -----------
        parameters:
            query: palavra chave da pesquisa
                query: "pesquisa" ou "pesquisa, subpesquisa" ou "#pesquisa"

            no_query: palavra chave que nao conste na pesquisa
                no_query: "-a, -b, -c" , "-a", etc.

            state: pesquisa por Estado
                state: "near:estado within:15mi"

            date: pesquisa por data
                date: "until:yyy-MM-dd since:yyyy-MM-dd" until:data_fim since data_inicio

            lang: pesquisa pelo idioma da pesquisa
                lang: "pt-br", "en", etc
            
            top_tweet: pesquisa por tweets mais recentes ou antigos
                 top_tweet: False(antigos) ou True(atuais)
    """
    
    name = 'TwitterScrapy'
    allowed_domains = ['twitter.com']

    def __init__(self, query='', no_query='', state='', date='', lang='pt-br', top_tweet=False):
    
        self.query = query
        self.no_query = no_query
        self.state = state
        self.date = date
        
        self.url = 'https://twitter.com/i/search/timeline?l={}'.format(lang)

        if not top_tweet:
            self.url = self.url + '&f=tweets'
    
        if no_query:
            self.url = self.url + '&q=%s %s&src=typed&max_position=%s'
        elif state:
            self.url = self.url + '&q=%s %s&src=typed&max_position=%s'
        elif date:
            self.url = self.url + '&q=%s %s&src=typed&max_position=%s'
        else:
            self.url = self.url + "&q=%s&src=typed&max_position=%s"
    
    def start_requests(self):
        if self.no_query:
            url = self.url % (quote(self.query), None, None)
        elif self.state:
            url = self.url % (quote(self.query), None, None)
        elif self.date:
            url = self.url % (quote(self.query), None, None)
        else:
            url = self.url % (quote(self.query), None)

        yield http.Request(url, callback=self.parse_page)
    
    def parse_page(self, response):
        data = json.loads(response.body.decode("utf-8"))
        for item in self.parse_tweets_block(data['items_html']):
            yield item
        
        min_position = data['min_position']
        min_position = min_position.replace("+", "%2B")


        if self.no_query:
            url = self.url % (quote(self.query), quote(self.no_query), min_position)
        elif self.state:
            url = self.url % (quote(self.query), quote(self.state), min_position)
        elif self.date:
            url = self.url % (quote(self.query), quote(self.date), min_position)
        else:
            url = self.url % (quote(self.query), min_position)

        yield http.Request(url, callback=self.parse_page)
    
    def parse_tweets_block(self, http_page):
        page = Selector(text=http_page)

        items = page.xpath('//li[@data-item-type="tweet"]/div')
        
        for item in self.parse_tweet_item(items):
            yield item


    def parse_tweet_item(self, items):
        for item in items:
            try:
                # instancia da classe Item
                tweet = TwitterItem()

                # Nome do tweet
                tweet['usernameTweet'] = item.xpath('.//span[@class="username u-dir u-textTruncate"]/b/text()').extract()[0]
                
                # ID do tweet
                tweet['user_id'] = item.xpath('.//@data-user-id').extract()[0]

                ID = item.xpath('.//@data-tweet-id').extract()

                if not ID:
                    continue

                tweet['ID'] = ID[0]

                # textos do tweet
                tweet['text'] = ''.join(
                    item.xpath('.//div[@class="js-tweet-text-container"]/p//text()').extract()).replace(' # ',
                                                                                                        '#').replace(
                    ' @ ', '@').replace('\n', ' ')
                                                                                                        
                if tweet['text'] == '':
                    # If there is not text, we ignore the tweet
                    continue

                # url do post do tweet
                tweet['url'] = item.xpath('.//@data-permalink-path').extract()[0]

                # data da postagem do tweet
                tweet['datetime'] = datetime.fromtimestamp(int(
                    item.xpath('.//div[@class="stream-item-header"]/small[@class="time"]/a/span/@data-time').extract()[
                        0])).strftime('%Y-%m-%d %H:%M:%S')

                # numero de retweet do post
                number_retweet = item.css('span.ProfileTweet-action--retweet > span.ProfileTweet-actionCount').xpath('@data-tweet-stat-count').extract()
                if number_retweet:
                    tweet['number_retweet'] = int(number_retweet[0])
                else:
                    tweet['number_retweet'] = 0

                # numero de liks do post
                number_favorite = item.css('span.ProfileTweet-action--favorite > span.ProfileTweet-actionCount').xpath('@data-tweet-stat-count').extract()
                if number_favorite:
                    tweet['number_favorite'] = int(number_favorite[0])
                else:
                    tweet['number_favorite'] = 0
                
                # numero de respostas do post
                number_reply = item.css('span.ProfileTweet-action--reply > span.ProfileTweet-actionCount').xpath('@data-tweet-stat-count').extract()
                if number_reply:
                    tweet['number_reply'] = int(number_reply[0])
                else:
                    tweet['number_reply'] = 0
                
                # Returna False se nao ha resposta e True caso tenha
                is_reply = item.xpath('.//div[@class="ReplyingToContextBelowAuthor"]').extract()
                tweet['is_reply'] = is_reply != []
                
                # Returna False se nao ha retweet e True caso tenha
                is_retweet = item.xpath('.//span[@class="js-retweet-text"]').extract()
                tweet['is_retweet'] = is_retweet != []

                yield tweet

            except:
                logger.error("Error tweet:\n%s" % item.xpath('.').extract()[0])
                # raise
