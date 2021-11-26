from crawler_manager_pb2 import KillResponse
from crawler_manager_pb2_grpc import add_CrawlerManagerServicer_to_server, CrawlerManagerServicer
from crawler_manager_pb2 import RegisterRequest, RegisterResponse, PullRequest, PullResponse
from concurrent import futures
import grpc

from collections import defaultdict, deque
from uuid import uuid4
from queue_connector import QueueConnector

queue_connector = QueueConnector()
class CrawlerManagerServicer(CrawlerManagerServicer):
  crawlers = defaultdict(lambda: None)

  def register(self, request, context):
    new_id = str(uuid4())
    self.crawlers[new_id] = deque()
    return RegisterResponse(status='OK', id=new_id)

  def pull(self, request, context):
    id = request.id
    if self.crawlers[id] is None: return PullResponse(status='NOREG')
    if len(self.crawlers[id]) < 3:
      self.crawlers[id].extend([link.decode('utf-8') for link in queue_connector.pop(10)])
    if len(self.crawlers[id]) < 1:
      return PullResponse(status='RETRY')
    return PullResponse(status='OK', url=self.crawlers[id].pop())

  def kill(self, request, context):
    print('Killing', flush=True)
    id = request.id
    queue = self.crawlers.pop(id, None)
    if queue is None: return KillResponse(status='OK')
    queue_connector.put_back(list(queue))
    return KillResponse(status='OK')




def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  add_CrawlerManagerServicer_to_server(CrawlerManagerServicer(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()

serve()
