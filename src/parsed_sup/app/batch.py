from db_processed import Keyword, session_factory, Url
from queue_connector import QueueConnector

session = session_factory()
queue = QueueConnector()

def process_batch(batch):
  all_urls = []
  all_keywords = []
  for item in batch:
    all_urls.append(item.url)
    all_keywords += item.keywords
  queue.push(all_urls)
  all_urls = _get_or_create_urls(all_urls)
  all_keywords = _get_or_create_keywords(list(set(all_keywords)))

  for item in batch:
    url = list(filter(lambda x: x.url == item.url, all_urls))[0]
    keywords = list(filter(lambda x: x.keyword in item.keywords, all_keywords))
    if (url.keywords is None):
      url.keywords = keywords
    else:
      url.keywords += keywords
  session.commit()
  # print("Batch processed", flush=True)

def _get_or_create_urls(urls):
  url_objs = list(session.query(Url).filter(Url.url.in_(urls)).all())
  urls_to_create = [url for url in urls if url not in list(map(lambda x: x.url, url_objs))]
  new_urls = [Url(url=url) for url in urls_to_create]
  session.add_all(new_urls)
  return url_objs + new_urls

def _get_or_create_keywords(keywords):
  keyword_objs = list(session.query(Keyword).filter(Keyword.keyword.in_(keywords)).all())
  keywords_to_create = [keyword for keyword in keywords if keyword not in list(map(lambda x: x.keyword, keyword_objs))]
  new_keywords = [Keyword(keyword=keyword) for keyword in keywords_to_create]
  session.add_all(new_keywords)
  return keyword_objs + new_keywords
