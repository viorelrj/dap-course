import scrapy
import grpc
from crawler_pb2_grpc import CrawlerSupervisorStub
from crawler_pb2 import SubmitRequest
import re
import string

translation_table = str.maketrans('', '', string.punctuation)

channel = grpc.insecure_channel('localhost:50051')
stub = CrawlerSupervisorStub(channel)


def flatten_list(list_of_lists):
  return [item for sublist in list_of_lists for item in sublist]


class BlogSpider(scrapy.Spider):
  name = 'blogspider'
  start_urls = ['https://www.zyte.com/blog/']

  def __init__(self,*args, **kwargs):
    super(BlogSpider, self).__init__(*args, **kwargs)

  def parse(self, response):
    important_sentences = list(map(lambda x: x.css('*::text').getall(), response.css('h1, h1 *, title, title *')))
    keywords_lists = list(map(lambda x: self._get_words(
        x), flatten_list(important_sentences)))
    keywords = flatten_list(keywords_lists)

    stub.submit.future(
      SubmitRequest(
        origin=response.url,
        links=list(filter(lambda x: len(x) > 1, set(response.css('a::attr(href)').extract()))),
        keywords=keywords
      ),
      wait_for_ready=True
    )
    # for title in response.css('.oxy-post-title'):
    #   pass
    for next_page in response.css('a[href]'):
      yield response.follow(next_page, self.parse)

  def _get_words(self, text):
    words = filter(lambda x: len(x), re.split(r'\W+', text))
    stripped = [w.translate(translation_table) for w in words]
    lowercase = [word.lower() for word in stripped]
    return lowercase


