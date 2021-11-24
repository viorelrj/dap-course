
from processed_sink_pb2_grpc import add_ProcessedSinkServicer_to_server, ProcessedSinkServicer
from processed_sink_pb2 import SubmitResponse
import grpc
from concurrent import futures
from queue import Queue
from rx.subject import Subject
from rx.operators import buffer_with_time_or_count
from batch import process_batch
from parsed_response import ParsedResponse
from queue_connector import QueueConnector


queue = QueueConnector()
batch = Queue()
db_dispatcher = Subject()
queue_dispatcher = Subject()

db_dispatcher.pipe(
  buffer_with_time_or_count(timespan=5.0, count=50)
).subscribe(lambda x: process_batch(x))

queue_dispatcher.pipe(
  buffer_with_time_or_count(timespan=5.0, count=50)
).subscribe(lambda x: process_queue_batch(x))

def process_queue_batch(batch):
  links = list(set(flatten_list(batch)))
  queue.push(links)
  
def flatten_list(list_of_lists):
  return [item for sublist in list_of_lists for item in sublist]

class ProcessedSinkServicer(ProcessedSinkServicer):
  def submit(self, request, context):
    print(request.links, flush=True)
    db_dispatcher.on_next(ParsedResponse(request.origin, list(set(request.keywords))))
    queue_dispatcher.on_next(list(request.links))
    return SubmitResponse()

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  add_ProcessedSinkServicer_to_server(ProcessedSinkServicer(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()

serve()

