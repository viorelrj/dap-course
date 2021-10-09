from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    'postgresql://ADMIN:ADMIN@processed_db:5432/processed').connect()
_SessionFactory = sessionmaker(bind=engine)
Base = declarative_base()

def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()


keywords_urls_assotiation = Table(
    'keywords_urls_assotiation', Base.metadata,
    Column('keyword', String, ForeignKey('keywords.keyword')),
    Column('url', String, ForeignKey('urls.url'))
)

class Keyword(Base):
  __tablename__ = 'keywords'
  keyword = Column(String, primary_key=True)
  

  def __init__(self, keyword):
    self.keyword = keyword

class Url(Base):
  __tablename__ = 'urls'
  url = Column(String, primary_key=True)
  keywords = relationship('Keyword', secondary=keywords_urls_assotiation)

  def __init__(self, url, keywords):
    self.url = url
    self.keywords = keywords
