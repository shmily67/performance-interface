# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: BusproxyTas1.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import common_pb2
import PublicTas1_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='BusproxyTas1.proto',
  package='BusproxyTas1',
  serialized_pb='\n\x12\x42usproxyTas1.proto\x12\x0c\x42usproxyTas1\x1a\x0c\x63ommon.proto\x1a\x10PublicTas1.proto\"K\n\rL2PStatusSync\x12\x1c\n\x06Header\x18\x01 \x01(\x0b\x32\x0c.MessageHead\x12\x0f\n\x07RetCode\x18\x02 \x01(\x05\x12\x0b\n\x03Nop\x18\x03 \x01(\x05')




_L2PSTATUSSYNC = _descriptor.Descriptor(
  name='L2PStatusSync',
  full_name='BusproxyTas1.L2PStatusSync',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='Header', full_name='BusproxyTas1.L2PStatusSync.Header', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='RetCode', full_name='BusproxyTas1.L2PStatusSync.RetCode', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='Nop', full_name='BusproxyTas1.L2PStatusSync.Nop', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=68,
  serialized_end=143,
)

_L2PSTATUSSYNC.fields_by_name['Header'].message_type = common_pb2._MESSAGEHEAD
DESCRIPTOR.message_types_by_name['L2PStatusSync'] = _L2PSTATUSSYNC

class L2PStatusSync(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _L2PSTATUSSYNC

  # @@protoc_insertion_point(class_scope:BusproxyTas1.L2PStatusSync)


# @@protoc_insertion_point(module_scope)