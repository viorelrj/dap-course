# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: crawler.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='crawler.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\rcrawler.proto\"@\n\rSubmitRequest\x12\x0e\n\x06origin\x18\x01 \x01(\t\x12\r\n\x05links\x18\x02 \x03(\t\x12\x10\n\x08keywords\x18\x03 \x03(\t\"\"\n\x0eSubmitResponse\x12\x10\n\x08response\x18\x01 \x01(\t2@\n\x11\x43rawlerSupervisor\x12+\n\x06submit\x12\x0e.SubmitRequest\x1a\x0f.SubmitResponse\"\x00\x62\x06proto3')
)




_SUBMITREQUEST = _descriptor.Descriptor(
  name='SubmitRequest',
  full_name='SubmitRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='origin', full_name='SubmitRequest.origin', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='links', full_name='SubmitRequest.links', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='keywords', full_name='SubmitRequest.keywords', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=81,
)


_SUBMITRESPONSE = _descriptor.Descriptor(
  name='SubmitResponse',
  full_name='SubmitResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='response', full_name='SubmitResponse.response', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=83,
  serialized_end=117,
)

DESCRIPTOR.message_types_by_name['SubmitRequest'] = _SUBMITREQUEST
DESCRIPTOR.message_types_by_name['SubmitResponse'] = _SUBMITRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SubmitRequest = _reflection.GeneratedProtocolMessageType('SubmitRequest', (_message.Message,), dict(
  DESCRIPTOR = _SUBMITREQUEST,
  __module__ = 'crawler_pb2'
  # @@protoc_insertion_point(class_scope:SubmitRequest)
  ))
_sym_db.RegisterMessage(SubmitRequest)

SubmitResponse = _reflection.GeneratedProtocolMessageType('SubmitResponse', (_message.Message,), dict(
  DESCRIPTOR = _SUBMITRESPONSE,
  __module__ = 'crawler_pb2'
  # @@protoc_insertion_point(class_scope:SubmitResponse)
  ))
_sym_db.RegisterMessage(SubmitResponse)



_CRAWLERSUPERVISOR = _descriptor.ServiceDescriptor(
  name='CrawlerSupervisor',
  full_name='CrawlerSupervisor',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=119,
  serialized_end=183,
  methods=[
  _descriptor.MethodDescriptor(
    name='submit',
    full_name='CrawlerSupervisor.submit',
    index=0,
    containing_service=None,
    input_type=_SUBMITREQUEST,
    output_type=_SUBMITRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_CRAWLERSUPERVISOR)

DESCRIPTOR.services_by_name['CrawlerSupervisor'] = _CRAWLERSUPERVISOR

# @@protoc_insertion_point(module_scope)
