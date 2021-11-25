from queue_connector import QueueConnector
from db_processed import Keyword, session_factory, Url

session = None
process_queue = QueueConnector()


def flatten_list(list_of_lists):
  return [item for sublist in list_of_lists for item in sublist]

def process_batch(batch):
  global session 
  session = session_factory()
  all_urls = []
  all_keywords = []
  all_next_links = []

  for item in batch:
    all_urls.append(item.url)
    all_keywords += item.keywords
    all_next_links += item.links
  all_urls = _get_or_create_urls(list(set(all_urls)))
  all_keywords = _get_or_create_keywords(list(set(all_keywords)))
  process_queue_batch(list(set(all_next_links)))

  for item in batch:
    url = list(filter(lambda x: x.url == item.url, all_urls))[0]
    keywords = list(filter(lambda x: x.keyword in item.keywords, all_keywords))
    if (url.keywords is None):
      url.keywords = keywords
    else:
      url.keywords += keywords
  session.commit()
  session.close()


def process_queue_batch(links):
  session = session_factory()
  dupe_links = list(session.query(Url).filter(Url.url.in_(links)).all())
  dupe_links = [link.url for link in dupe_links]
  links = [link for link in links if link not in dupe_links]
  print(links, flush=True)
  process_queue.push(links)


def _get_or_create_urls(urls):
  url_objs = list(session.query(Url).filter(Url.url.in_(urls)).all())
  existing_urls = list(map(lambda x: x.url, url_objs))
  urls_to_create = [url for url in urls if url not in existing_urls]
  new_urls = [Url(url=url) for url in urls_to_create]
  session.add_all(new_urls)
  return url_objs + new_urls

def _get_or_create_keywords(keywords):
  keyword_objs = list(session.query(Keyword).filter(Keyword.keyword.in_(keywords)).all())
  keywords_to_create = [keyword for keyword in keywords if keyword not in list(map(lambda x: x.keyword, keyword_objs))]
  new_keywords = [Keyword(keyword=keyword) for keyword in keywords_to_create]
  session.add_all(new_keywords)
  return keyword_objs + new_keywords
