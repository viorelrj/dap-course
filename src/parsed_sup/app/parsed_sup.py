from sqlalchemy.orm import sessionmaker
from crawler_pb2_grpc import add_CrawlerSupervisorServicer_to_server, CrawlerSupervisorServicer
from crawler_pb2 import SubmitResponse
import grpc
from concurrent import futures
from db_processed import Keyword, session_factory

session = session_factory()

# session.add(Keyword(keyword='test'))
# session.commit()
# session.close()


class CrawlerSupervisorServicer(CrawlerSupervisorServicer):
  def submit(self, request, context):
    print(request, flush=True)
    return SubmitResponse()


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  add_CrawlerSupervisorServicer_to_server(CrawlerSupervisorServicer(), server)
  session.add(Keyword(keyword='test'))
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()


serve()
