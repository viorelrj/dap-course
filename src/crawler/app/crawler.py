import scrapy
import grpc
from crawler_manager_pb2 import KillRequest
from processed_sink_pb2_grpc import ProcessedSinkStub
from processed_sink_pb2 import SubmitRequest
from crawler_manager_pb2_grpc import CrawlerManagerStub
from crawler_manager_pb2 import RegisterRequest, PullRequest
from time import sleep

import re
import string

translation_table = str.maketrans('', '', string.punctuation)

processed_sink_channel = grpc.insecure_channel('parsed_sup:50051')
processed_sink_stub = ProcessedSinkStub(processed_sink_channel)

crawler_manager_channel = grpc.insecure_channel('crawler_manager:50051')
crawler_manager_stub = CrawlerManagerStub(crawler_manager_channel)


def flatten_list(list_of_lists):
  return [item for sublist in list_of_lists for item in sublist]


class CircuitBreaker:
  def reset(self):
    self.tries = 0

  def __init__(self, max_tries, sleep_time):
    self.max_tries = max_tries
    self.sleep_time = sleep_time
    self.reset()

  def can_try(self):
    return self.tries < self.max_tries

  def time_till_next(self):
    time = self.sleep_time * self.tries * 2**self.tries
    self.tries += 1
    return time


class BlogSpider(scrapy.Spider):
  name = 'blogspider'
  custom_settings = {
    'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
  }
  start_urls = ['https://www.zyte.com/blog/']
  id = ''

  def get_next_page(self):
    cb = CircuitBreaker(5, 1)
    manager_response = crawler_manager_stub.pull(PullRequest(id=self.id))
    while (manager_response.status == 'RETRY' and cb.can_try()):
      sleep(cb.time_till_next())
      manager_response = crawler_manager_stub.pull(PullRequest(id=self.id))
    return manager_response.url

  def __init__(self,*args, **kwargs):
    super(BlogSpider, self).__init__(*args, **kwargs)
    self.id = crawler_manager_stub.register(RegisterRequest(id=''), wait_for_ready=True).id

  def parse(self, response):
    important_sentences = list(map(lambda x: x.css('*::text').getall(), response.css('h1, h1 *, title, title *')))
    keywords_lists = list(map(lambda x: self._get_words(
        x), flatten_list(important_sentences)))
    keywords = flatten_list(keywords_lists)

    links = list(filter(lambda x: len(x) > 1, set(
        response.css('a::attr(href)').extract())))
    links = [response.urljoin(link) for link in links]

    processed_sink_stub.submit(
      SubmitRequest(
        origin=response.url,
        links=links,
        keywords=keywords
      )
    )
    print(response.url, flush=True)
    yield response.follow(self.get_next_page(), self.parse, errback=lambda x: self.handle_exception(x, response))

  def handle_exception(self, err, response):
    response.follow(self.get_next_page(), self.parse, errback=lambda x: self.handle_exception(x, response))

  def closed(self, reason):
    crawler_manager_stub.kill(KillRequest(id=self.id))


  def _get_words(self, text):
    words = filter(lambda x: len(x), re.split(r'\W+', text))
    stripped = [w.translate(translation_table) for w in words]
    lowercase = [word.lower() for word in stripped]
    return list(dict.fromkeys(lowercase))


