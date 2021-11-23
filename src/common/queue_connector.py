
from redis import Redis, ConnectionPool
import asyncio



class QueueConnector:
  async def get_connection(self):
    conn = Redis(host='crawler_queue', port=6379, db=0)
    ping = False
    while ping == False:
      try:
        ping = conn.ping()
      except:
        pass
      asyncio.sleep(1)
    return conn

  def __init__(self):
    connection = asyncio.run(self.get_connection())
    self.redis = Redis(connection_pool=connection)

  def get_first(self, n):
    self.redis.lrange('queue_to_process', 0, n)

  def push(self, items):
    print(items, flush=True)
    self.redis.rpush('queue_to_process', *items)

  def pop(self, n):
    with self.redis.pipeline() as pipe:
      items = pipe.lrange('queue_to_process', 0, n)
      pipe.ltrim('queue_to_process', 0, n)
      pipe.execute()
      pipe.reset()
      return items
