from flask import Flask
from flask_restful import Resource, Api
from db_processed import Keyword, session_factory

app = Flask(__name__)
api = Api(app)

def flatten_list(l):
  return [item for sublist in l for item in sublist]

def get_urls_related_to_keywords(keywords):
  session = session_factory()
  urls = flatten_list([k.urls for k in session.query(Keyword).filter(Keyword.keyword.in_(keywords)) ])
  session.close()
  return [u.url for u in urls]

class HelloWorld(Resource):
  def get(self, keywords):
    print("Viorel", flush=True)
    return get_urls_related_to_keywords(keywords.split())


api.add_resource(HelloWorld, '/<string:keywords>')

if __name__ == '__main__':
  app.run(host='0.0.0.0')
