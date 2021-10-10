from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
  'postgresql://ADMIN:ADMIN@processed_db:5432/processed', echo=True, pool_size=50).connect()
_SessionFactory = sessionmaker(bind=engine, autoflush=True)
Base = declarative_base()


def session_factory():
  Base.metadata.create_all(engine)
  return _SessionFactory()

association_table = Table('association', Base.metadata,
  Column('url', ForeignKey('urls.url'), primary_key=False),
  Column('keyword', ForeignKey('keywords.keyword'), primary_key=False)
)

class Keyword(Base):
  __tablename__ = 'keywords'
  keyword = Column(String, primary_key=True)
  urls = relationship('Url', secondary=association_table, back_populates='keywords')

  def __init__(self, keyword):
    self.keyword = keyword

class Url(Base):
  __tablename__ = 'urls'
  url = Column(String, primary_key=True)
  keywords = relationship('Keyword', secondary=association_table, back_populates='urls')

  def __init__(self, url):
    self.url = url
