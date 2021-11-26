from redis import Redis

class QueueConnector:
  redis = Redis(host='crawler_queue', port=6379, db=0)

  def get_first(self, n):
    return self.redis.lrange('queue_to_process', 0, n - 1)

  def push(self, items):
    if not len(items): return
    self.redis.rpush('queue_to_process', *items)

  def put_back(self, items):
    if not len(items): return
    self.redis.lpush('queue_to_process', *items)

  def pop(self, n):
    pipe = self.redis.pipeline()
    pipe.lrange('queue_to_process', 0, n - 1)
    pipe.ltrim('queue_to_process', n, -1)
    res = pipe.execute()
    pipe.reset()
    return res[0]
