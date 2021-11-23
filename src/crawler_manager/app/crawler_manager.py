from crawler_manager_pb2_grpc import add_CrawlerManagerServicer_to_server, CrawlerManagerServicer
from crawler_manager_pb2 import RegisterRequest, RegisterResponse, PullRequest, PullResponse
from queue import Queue
from concurrent import futures
import grpc

from collections import defaultdict
from uuid import uuid4
class CrawlerManagerServicer(CrawlerManagerServicer):
  crawlers = defaultdict(lambda: None)

  def register(self, request, context):
    new_id = str(uuid4())
    self.crawlers[new_id] = Queue()
    self.crawlers[new_id].put('http://www.google.com')
    return RegisterResponse(status='OK', id=new_id)

  def pull(self, request, context):
    id = request.id
    if self.crawlers[id] is None: return PullResponse(status='NOREG')
    # if self.crawlers[id].qsize() < 3:
      # pull from redis
    if self.crawlers[id].qsize() < 1:
      return PullResponse(status='RETRY')
    return PullResponse(status='OK', url=self.crawlers[id].get())


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  add_CrawlerManagerServicer_to_server(CrawlerManagerServicer(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()

serve()
