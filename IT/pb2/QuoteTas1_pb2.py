# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: QuoteTas1.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import common_pb2
import PublicTas1_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='QuoteTas1.proto',
  package='QuoteTas1',
  serialized_pb='\n\x0fQuoteTas1.proto\x12\tQuoteTas1\x1a\x0c\x63ommon.proto\x1a\x10PublicTas1.proto\"\x81\x05\n\tQuotation\x12\x1c\n\x06Header\x18\x01 \x01(\x0b\x32\x0c.MessageHead\x12\x0f\n\x07RetCode\x18\x02 \x01(\x05\x12\x11\n\tGoodsCode\x18\x03 \x01(\t\x12\x11\n\tGoodsName\x18\x04 \x01(\t\x12\x0c\n\x04Last\x18\x05 \x01(\t\x12\x12\n\nLastVolume\x18\x06 \x01(\t\x12\x14\n\x0cLastTurnover\x18\x07 \x01(\t\x12\x0f\n\x07LastLot\x18\x08 \x01(\t\x12\x13\n\x0bTotalVolume\x18\t \x01(\t\x12\x15\n\rTotalTurnover\x18\n \x01(\t\x12\x10\n\x08TotalLot\x18\x0b \x01(\t\x12\x0b\n\x03\x42id\x18\x0c \x01(\t\x12\x0c\n\x04\x42id2\x18\r \x01(\t\x12\x0c\n\x04\x42id3\x18\x0e \x01(\t\x12\x0c\n\x04\x42id4\x18\x0f \x01(\t\x12\x0c\n\x04\x42id5\x18\x10 \x01(\t\x12\x11\n\tBidVolume\x18\x11 \x01(\t\x12\x12\n\nBidVolume2\x18\x12 \x01(\t\x12\x12\n\nBidVolume3\x18\x13 \x01(\t\x12\x12\n\nBidVolume4\x18\x14 \x01(\t\x12\x12\n\nBidVolume5\x18\x15 \x01(\t\x12\x0b\n\x03\x41sk\x18\x16 \x01(\t\x12\x0c\n\x04\x41sk2\x18\x17 \x01(\t\x12\x0c\n\x04\x41sk3\x18\x18 \x01(\t\x12\x0c\n\x04\x41sk4\x18\x19 \x01(\t\x12\x0c\n\x04\x41sk5\x18\x1a \x01(\t\x12\x11\n\tAskVolume\x18\x1b \x01(\t\x12\x12\n\nAskVolume2\x18\x1c \x01(\t\x12\x12\n\nAskVolume3\x18\x1d \x01(\t\x12\x12\n\nAskVolume4\x18\x1e \x01(\t\x12\x12\n\nAskVolume5\x18\x1f \x01(\t\x12\x11\n\tTradeDate\x18  \x01(\t\x12\x0c\n\x04Time\x18! \x01(\t\x12\x12\n\nExchangeID\x18\" \x01(\x05\x12\x13\n\x0bWareGroupID\x18# \x01(\x05')




_QUOTATION = _descriptor.Descriptor(
  name='Quotation',
  full_name='QuoteTas1.Quotation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='Header', full_name='QuoteTas1.Quotation.Header', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='RetCode', full_name='QuoteTas1.Quotation.RetCode', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='GoodsCode', full_name='QuoteTas1.Quotation.GoodsCode', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='GoodsName', full_name='QuoteTas1.Quotation.GoodsName', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='Last', full_name='QuoteTas1.Quotation.Last', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='LastVolume', full_name='QuoteTas1.Quotation.LastVolume', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='LastTurnover', full_name='QuoteTas1.Quotation.LastTurnover', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='LastLot', full_name='QuoteTas1.Quotation.LastLot', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='TotalVolume', full_name='QuoteTas1.Quotation.TotalVolume', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='TotalTurnover', full_name='QuoteTas1.Quotation.TotalTurnover', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='TotalLot', full_name='QuoteTas1.Quotation.TotalLot', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='Bid', full_name='QuoteTas1.Quotation.Bid', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='Bid2', full_name='QuoteTas1.Quotation.Bid2', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='Bid3', full_name='QuoteTas1.Quotation.Bid3', index=13,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='Bid4', full_name='QuoteTas1.Quotation.Bid4', index=14,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='Bid5', full_name='QuoteTas1.Quotation.Bid5', index=15,
      number=16, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='BidVolume', full_name='QuoteTas1.Quotation.BidVolume', index=16,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='BidVolume2', full_name='QuoteTas1.Quotation.BidVolume2', index=17,
      number=18, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='BidVolume3', full_name='QuoteTas1.Quotation.BidVolume3', index=18,
      number=19, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='BidVolume4', full_name='QuoteTas1.Quotation.BidVolume4', index=19,
      number=20, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='BidVolume5', full_name='QuoteTas1.Quotation.BidVolume5', index=20,
      number=21, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='Ask', full_name='QuoteTas1.Quotation.Ask', index=21,
      number=22, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='Ask2', full_name='QuoteTas1.Quotation.Ask2', index=22,
      number=23, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='Ask3', full_name='QuoteTas1.Quotation.Ask3', index=23,
      number=24, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='Ask4', full_name='QuoteTas1.Quotation.Ask4', index=24,
      number=25, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='Ask5', full_name='QuoteTas1.Quotation.Ask5', index=25,
      number=26, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='AskVolume', full_name='QuoteTas1.Quotation.AskVolume', index=26,
      number=27, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='AskVolume2', full_name='QuoteTas1.Quotation.AskVolume2', index=27,
      number=28, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='AskVolume3', full_name='QuoteTas1.Quotation.AskVolume3', index=28,
      number=29, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='AskVolume4', full_name='QuoteTas1.Quotation.AskVolume4', index=29,
      number=30, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='AskVolume5', full_name='QuoteTas1.Quotation.AskVolume5', index=30,
      number=31, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='TradeDate', full_name='QuoteTas1.Quotation.TradeDate', index=31,
      number=32, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='Time', full_name='QuoteTas1.Quotation.Time', index=32,
      number=33, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ExchangeID', full_name='QuoteTas1.Quotation.ExchangeID', index=33,
      number=34, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='WareGroupID', full_name='QuoteTas1.Quotation.WareGroupID', index=34,
      number=35, type=5, cpp_type=1, label=1,
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
  serialized_start=63,
  serialized_end=704,
)

_QUOTATION.fields_by_name['Header'].message_type = common_pb2._MESSAGEHEAD
DESCRIPTOR.message_types_by_name['Quotation'] = _QUOTATION

class Quotation(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _QUOTATION

  # @@protoc_insertion_point(class_scope:QuoteTas1.Quotation)


# @@protoc_insertion_point(module_scope)