import scrapy
import grpc
from crawler_pb2_grpc import CrawlerSupervisorStub
from crawler_pb2 import SubmitRequest

channel = grpc.insecure_channel('parsed_sup:50051')
stub = CrawlerSupervisorStub(channel)


class BlogSpider(scrapy.Spider):
  name = 'blogspider'
  start_urls = ['https://www.zyte.com/blog/']

  def __init__(self,*args, **kwargs):
    super(BlogSpider, self).__init__(*args, **kwargs)

  def parse(self, response):
    stub.submit.future(SubmitRequest(
        origin='https://www.google.com'), wait_for_ready=True)
    for title in response.css('.oxy-post-title'):
      pass
    for next_page in response.css('a.next'):
      yield response.follow(next_page, self.parse)

