from sqlalchemy.orm import sessionmaker
from crawler_pb2_grpc import add_CrawlerSupervisorServicer_to_server, CrawlerSupervisorServicer
from crawler_pb2 import SubmitResponse
import grpc
from concurrent import futures
from db_processed import Keyword, session_factory, Url



# def add_only_new_keywords(keywords):
#   session = session_factory()
#   existing_keywords = session.query(Keyword).filter(Keyword.keyword.in_(keywords)).all()
#   new_keywords = list(filter(lambda x: x not in existing_keywords, keywords))

#   if len(new_keywords):
#     session.add_all([Keyword(keyword=keyword) for keyword in new_keywords])
#     session.commit()
#     session.close()


# def add_only_new_urls(urls):
#   session = session_factory()
#   existing_urls = session.query(Url).filter(Url.url.in_(urls)).all()
#   new_urls = list(filter(lambda x: x not in existing_urls, urls))

#   if len(new_urls):
#     session.add_all([Url(url=url) for url in new_urls])
#     session.commit()
#     session.close()





class CrawlerSupervisorServicer(CrawlerSupervisorServicer):
  def submit(self, request, context):
    session = session_factory()
    keywords_to_add = [Keyword(keyword=keyword) for keyword in request.keywords]
    url = Url(request.origin, keywords_to_add)
    session.add(url)
    session.commit()
    session.close()
    print('Here', flush=True)

    return SubmitResponse()


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  add_CrawlerSupervisorServicer_to_server(CrawlerSupervisorServicer(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()

serve()
