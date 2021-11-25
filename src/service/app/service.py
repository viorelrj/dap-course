from flask import Flask, make_response
from flask_restful import Resource, Api
from db_processed import Keyword, session_factory
from redis import Redis
import json

app = Flask(__name__)
api = Api(app)
redis = Redis(host='service_cache', port=6379, db=0)

def flatten_list(l):
  return [item for sublist in l for item in sublist]


def get_cache_key(keywords):
  return keywords.lower().replace(' ', '_')

class LinksByKeywords(Resource):
  def get(self, keywords):
    cache_key = get_cache_key(keywords)
    cache_response = redis.get(cache_key)
    if cache_response:
      items = json.loads(cache_response.decode())
      return list(filter(lambda x: x is not None, items)), 200, {'X-Cache': 'HIT'}

    session = session_factory()
    urls = flatten_list([k.urls for k in session.query(
        Keyword).filter(Keyword.keyword.in_(keywords.split()))])
    session.close()
    url_strings = [u.url for u in urls]
    redis.set(cache_key, json.dumps(url_strings).encode() if url_strings else '[]'.encode())

    return url_strings, 200, {'X-Cache': 'MISS'}


api.add_resource(LinksByKeywords, '/<string:keywords>')

if __name__ == '__main__':
  app.run(host='0.0.0.0')
