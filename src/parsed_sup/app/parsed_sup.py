
from crawler_pb2_grpc import add_CrawlerSupervisorServicer_to_server, CrawlerSupervisorServicer
from crawler_pb2 import SubmitResponse
import grpc
from concurrent import futures
from db_processed import Keyword, session_factory, Url

session = session_factory()

def get_or_create_url(url):
  url_obj = session.query(Url).filter_by(url=url).first()
  if url_obj is None:
    url_obj = Url(url=url)
    session.add(url_obj)
    session.commit()
  return url_obj

def get_or_create_keywords(keywords):
  keywords_obj = []
  for keyword in keywords:
    keyword_obj = session.query(Keyword).filter_by(keyword=keyword).first()
    if keyword_obj is None:
      keyword_obj = Keyword(keyword=keyword)
      session.add(keyword_obj)
      session.commit()
    keywords_obj.append(keyword_obj)
  return keywords_obj

def add_url_keyword_relation(url, keywords):
  if (url.keywords is None):
    url.keywords = keywords
  else:
    url.keywords += keywords
  session.commit()
  print("COMMITTED this", flush=True)

class CrawlerSupervisorServicer(CrawlerSupervisorServicer):
  def submit(self, request, context):
    url = get_or_create_url(request.origin)
    keywords = get_or_create_keywords(list(set(request.keywords)))
    add_url_keyword_relation(url, keywords)
    session.commit()


    return SubmitResponse()


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
  add_CrawlerSupervisorServicer_to_server(CrawlerSupervisorServicer(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()

serve()
