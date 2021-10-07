import scrapy
import grpc
from crawler_pb2_grpc import CrawlerSupervisorStub
from crawler_pb2 import SubmitRequest
import re
import string

table = str.maketrans('', '', string.punctuation)

channel = grpc.insecure_channel('parsed_sup:50051')
stub = CrawlerSupervisorStub(channel)


class BlogSpider(scrapy.Spider):
  name = 'blogspider'
  start_urls = ['https://www.zyte.com/blog/']

  def __init__(self,*args, **kwargs):
    super(BlogSpider, self).__init__(*args, **kwargs)

  def parse(self, response):
    important_sentences = list(map(lambda x: x.css('*::text').getall(), response.css('h1, h1 *, title, title *')))
    keywords = list(map(lambda x: self._get_words(
        x), [item for sublist in important_sentences for item in sublist]))

    stub.submit.future(
      SubmitRequest(
        origin=response.url,
        links=list(filter(lambda x: len(x) > 1, set(response.css('a::attr(href)').extract()))),
        keywords=['test']
      ),
      wait_for_ready=True
    )
    # for title in response.css('.oxy-post-title'):
    #   pass
    for next_page in response.css('a'):
      yield response.follow(next_page, self.parse)

  def _get_words(self, text):
    words = filter(lambda x: len(x), re.split(r'\W+', text))
    stripped = [w.translate(table) for w in words]
    lowercase = [word.lower() for word in stripped]
    return lowercase
