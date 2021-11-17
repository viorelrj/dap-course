from crawler_manager_pb2_grpc import add_CrawlerManagerServicer_to_server, CrawlerManagerServicer
from crawler_manager_pb2 import RegisterRequest, RegisterResponse, PullRequest, PullResponse
from concurrent import futures

import grpc


class CrawlerManagerServicer(CrawlerManagerServicer):
  def register(self, request, context):
    print('register', flush=True)
    return RegisterResponse(status='OK')

  def pull(self, request, context):
    print('pull')
    return PullResponse(status='OK', url='http://www.google.com')


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  add_CrawlerManagerServicer_to_server(CrawlerManagerServicer(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()

serve()