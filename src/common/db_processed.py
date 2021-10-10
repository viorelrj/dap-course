from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Integer
import uuid

engine = create_engine(
  'postgresql://ADMIN:ADMIN@processed_db:5432/processed', echo=True, pool_size=10).connect()
_SessionFactory = sessionmaker(bind=engine, autoflush=True)
Base = declarative_base()


def session_factory():
  Base.metadata.create_all(engine)
  return _SessionFactory()

class UrlKeywordRelation(Base):
  __tablename__ = 'keywords_urls_relation'

  id = Column(String, primary_key=True)
  keyword = Column(String, ForeignKey('keywords.keyword'), primary_key=False)
  url = Column(String, ForeignKey('urls.url'), primary_key=False)

  def __init__(self, url, keyword):
    self.id = uuid.uuid4
    self.url = url
    self.keyword = keyword

class Keyword(Base):
  __tablename__ = 'keywords'
  keyword = Column(String, primary_key=True)
  urls = relationship('Url', secondary='keywords_urls_relation')

  def __init__(self, keyword):
    self.keyword = keyword

class Url(Base):
  __tablename__ = 'urls'
  url = Column(String, primary_key=True)
  keywords = relationship('Keyword', secondary='keywords_urls_relation')

  def __init__(self, url):
    self.url = url
