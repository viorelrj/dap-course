from flask import Flask, make_response
from flask_restful import Resource, Api
from db_processed import Keyword, session_factory
from redis import Redis

r = Redis(host='service_cache', port=6379)

app = Flask(__name__)
api = Api(app)

def flatten_list(l):
  return [item for sublist in l for item in sublist]


def get_cache_key(keywords):
  return keywords.lower().replace(' ', '_')


class LinksByKeywords(Resource):
  def get(self, keywords):
    cache_key = get_cache_key(keywords)
    cache_response = r.lrange(cache_key, 0, -1)
    if cache_response:
      print('Sending from cache', flush=True)
      items = [x.decode('utf-8') if x else None for x in cache_response]
      return list(filter(lambda x: x is not None, items)), 200, {'X-Cache': 'HIT'}

    session = session_factory()
    urls = flatten_list([k.urls for k in session.query(
        Keyword).filter(Keyword.keyword.in_(keywords.split()))])
    session.close()
    url_strings = [u.url for u in urls]
    r.lpush(cache_key, *url_strings if url_strings else [''])


    return url_strings, 200, {'X-Cache': 'MISS'}


api.add_resource(LinksByKeywords, '/<string:keywords>')

if __name__ == '__main__':
  app.run(host='0.0.0.0')
