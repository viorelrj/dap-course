import scrapy

class BlogSpider(scrapy.Spider):
  name = 'blogspider'
  start_urls = ['https://www.zyte.com/blog/']

  def __init__(self,*args, **kwargs):
    super(BlogSpider, self).__init__(*args, **kwargs)

  def parse(self, response):
    for title in response.css('.oxy-post-title'):
      print({'title': title.css('::text').get()})

    for next_page in response.css('a.next'):
      yield response.follow(next_page, self.parse)



# import grpc
# from crawler_pb2_grpc import CrawlerSupervisorStub
# from crawler_pb2 import SubmitRequest


# with grpc.insecure_channel('localhost:50051') as channel:
#   stub = CrawlerSupervisorStub(channel)
#   print(stub)
#   res = stub.submit(SubmitRequest(origin='https://www.google.com',
#               links=['https://www.google.com/1', 'https://www.google.com/2'], keywords=['google', 'search']))
#   print(res)






