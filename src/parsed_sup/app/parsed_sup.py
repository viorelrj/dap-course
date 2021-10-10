from sqlalchemy.orm import sessionmaker
from crawler_pb2_grpc import add_CrawlerSupervisorServicer_to_server, CrawlerSupervisorServicer
from crawler_pb2 import SubmitResponse
import grpc
from concurrent import futures
from db_processed import Keyword, session_factory, Url, UrlKeywordRelation

session = session_factory()

def add_url_if_not_exist(url):
  url_obj = session.query(Url).filter_by(url=url).first()
  if url_obj is None:
    url_obj = Url(url=url)
    session.add(url_obj)
    session.commit()

def add_keywords_if_not_exist(keywords):
  existing_keywords = session.query(Keyword).filter(Keyword.keyword.in_(keywords)).all()
  test = [w.keyword for w in existing_keywords]
  keywords_to_add = filter(lambda x: x not in test, keywords)
  session.add_all(map(lambda x: Keyword(x), keywords_to_add))
  session.commit()


def add_url_keyword_relation(url, keywords):
  for kw in keywords:
    session.merge(UrlKeywordRelation(url, kw))
  session.commit()
  print("COMMITTED this")

class CrawlerSupervisorServicer(CrawlerSupervisorServicer):
  def submit(self, request, context):
    keywords = list(set(request.keywords))
    add_url_if_not_exist(request.origin)
    add_keywords_if_not_exist(keywords)
    add_url_keyword_relation(request.origin, keywords)

    return SubmitResponse()


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  add_CrawlerSupervisorServicer_to_server(CrawlerSupervisorServicer(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()

serve()
