from crawler_pb2_grpc import add_CrawlerSupervisorServicer_to_server, CrawlerSupervisorServicer
from crawler_pb2 import SubmitResponse
import grpc
from concurrent import futures
from random import random


class CrawlerSupervisorServicer(CrawlerSupervisorServicer):
  def submit(self, request, context):
    print(random(), list(request.links))
    return SubmitResponse()


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  add_CrawlerSupervisorServicer_to_server(CrawlerSupervisorServicer(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()

serve()
