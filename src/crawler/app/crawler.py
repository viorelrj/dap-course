import scrapy
import grpc
from processed_sink_pb2_grpc import ProcessedSinkStub
from processed_sink_pb2 import SubmitRequest
from crawler_manager_pb2_grpc import CrawlerManagerStub
from crawler_manager_pb2 import RegisterRequest

import re
import string

translation_table = str.maketrans('', '', string.punctuation)

processed_sink_channel = grpc.insecure_channel('parsed_sup:50051')
processed_sink_stub = ProcessedSinkStub(processed_sink_channel)

crawler_manager_channel = grpc.insecure_channel('crawler_manager:50051')
crawler_manager_stub = CrawlerManagerStub(crawler_manager_channel)


def flatten_list(list_of_lists):
  return [item for sublist in list_of_lists for item in sublist]


class BlogSpider(scrapy.Spider):
  name = 'blogspider'
  start_urls = ['https://www.zyte.com/blog/']

  def __init__(self,*args, **kwargs):
    super(BlogSpider, self).__init__(*args, **kwargs)
    crawler_manager_stub.register(RegisterRequest(id=''), wait_for_ready=True)

  def parse(self, response):
    important_sentences = list(map(lambda x: x.css('*::text').getall(), response.css('h1, h1 *, title, title *')))
    keywords_lists = list(map(lambda x: self._get_words(
        x), flatten_list(important_sentences)))
    keywords = flatten_list(keywords_lists)

    processed_sink_stub.submit.future(
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
    return list(dict.fromkeys(lowercase))


