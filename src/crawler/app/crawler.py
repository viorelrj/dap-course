import scrapy
import grpc
from crawler_pb2_grpc import CrawlerSupervisorStub
from crawler_pb2 import SubmitRequest

channel = grpc.insecure_channel('localhost:3001')
stub = CrawlerSupervisorStub(channel)
stub.submit(SubmitRequest(origin='Ayo I am a test \n\n\n That\'s testig \n\n\n\n'))

class BlogSpider(scrapy.Spider):
  name = 'blogspider'
  start_urls = ['https://www.zyte.com/blog/']

  def __init__(self,*args, **kwargs):
    super(BlogSpider, self).__init__(*args, **kwargs)
    print('test', flush=True)


  def parse(self, response):
    for title in response.css('.oxy-post-title'):
      pass

    for next_page in response.css('a.next'):
      yield response.follow(next_page, self.parse)



# with grpc.insecure_channel('localhost:50051') as channel:
#   stub = CrawlerSupervisorStub(channel)
#   print(stub)
#   res = stub.submit(SubmitRequest(origin='https://www.google.com',
#               links=['https://www.google.com/1', 'https://www.google.com/2'], keywords=['google', 'search']))
#   print(res)






