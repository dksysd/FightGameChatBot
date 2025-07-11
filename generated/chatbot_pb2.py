# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: chatbot.proto
# Protobuf Python Version: 6.31.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    0,
    '',
    'chatbot.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rchatbot.proto\x12\x07\x63hatbot\"%\n\x12HealthCheckRequest\x12\x0f\n\x07service\x18\x01 \x01(\t\"\xa2\x01\n\x13HealthCheckResponse\x12:\n\x06status\x18\x01 \x01(\x0e\x32*.chatbot.HealthCheckResponse.ServingStatus\"O\n\rServingStatus\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0b\n\x07SERVING\x10\x01\x12\x0f\n\x0bNOT_SERVING\x10\x02\x12\x13\n\x0fSERVICE_UNKNOWN\x10\x03\"i\n\x12InitSessionRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12\x16\n\x0e\x63haracter_role\x18\x02 \x01(\t\x12\x15\n\ropponent_role\x18\x03 \x01(\t\x12\x10\n\x08language\x18\x04 \x01(\t\"Q\n\x13InitSessionResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x12\n\nsession_id\x18\x02 \x01(\t\x12\x15\n\rerror_message\x18\x03 \x01(\t\"7\n\x0b\x43hatRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12\x14\n\x0cuser_message\x18\x02 \x01(\t\"W\n\x0c\x43hatResponse\x12\x0e\n\x06speech\x18\x01 \x01(\t\x12\x0f\n\x07\x65motion\x18\x02 \x01(\t\x12\x0f\n\x07success\x18\x03 \x01(\x08\x12\x15\n\rerror_message\x18\x04 \x01(\t\"?\n\x0f\x41nalysisRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12\x18\n\x10opponent_actions\x18\x02 \x01(\t\"L\n\x10\x41nalysisResponse\x12\x10\n\x08\x61nalysis\x18\x01 \x01(\t\x12\x0f\n\x07success\x18\x02 \x01(\x08\x12\x15\n\rerror_message\x18\x03 \x01(\t\"\'\n\x11\x45ndSessionRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\"<\n\x12\x45ndSessionResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x15\n\rerror_message\x18\x02 \x01(\t\"\x15\n\x13ListSessionsRequest\"+\n\x14ListSessionsResponse\x12\x13\n\x0bsession_ids\x18\x01 \x03(\t2\xb1\x03\n\x14\x43haracterChatService\x12H\n\x0bInitSession\x12\x1b.chatbot.InitSessionRequest\x1a\x1c.chatbot.InitSessionResponse\x12\x33\n\x04\x43hat\x12\x14.chatbot.ChatRequest\x1a\x15.chatbot.ChatResponse\x12G\n\x10\x41nalyzeGameState\x12\x18.chatbot.AnalysisRequest\x1a\x19.chatbot.AnalysisResponse\x12\x45\n\nEndSession\x12\x1a.chatbot.EndSessionRequest\x1a\x1b.chatbot.EndSessionResponse\x12K\n\x0cListSessions\x12\x1c.chatbot.ListSessionsRequest\x1a\x1d.chatbot.ListSessionsResponse\x12=\n\nStreamChat\x12\x14.chatbot.ChatRequest\x1a\x15.chatbot.ChatResponse(\x01\x30\x01\x32\x92\x01\n\x06Health\x12\x42\n\x05\x43heck\x12\x1b.chatbot.HealthCheckRequest\x1a\x1c.chatbot.HealthCheckResponse\x12\x44\n\x05Watch\x12\x1b.chatbot.HealthCheckRequest\x1a\x1c.chatbot.HealthCheckResponse0\x01\x42\tZ\x07\x63hatbotb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chatbot_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\007chatbot'
  _globals['_HEALTHCHECKREQUEST']._serialized_start=26
  _globals['_HEALTHCHECKREQUEST']._serialized_end=63
  _globals['_HEALTHCHECKRESPONSE']._serialized_start=66
  _globals['_HEALTHCHECKRESPONSE']._serialized_end=228
  _globals['_HEALTHCHECKRESPONSE_SERVINGSTATUS']._serialized_start=149
  _globals['_HEALTHCHECKRESPONSE_SERVINGSTATUS']._serialized_end=228
  _globals['_INITSESSIONREQUEST']._serialized_start=230
  _globals['_INITSESSIONREQUEST']._serialized_end=335
  _globals['_INITSESSIONRESPONSE']._serialized_start=337
  _globals['_INITSESSIONRESPONSE']._serialized_end=418
  _globals['_CHATREQUEST']._serialized_start=420
  _globals['_CHATREQUEST']._serialized_end=475
  _globals['_CHATRESPONSE']._serialized_start=477
  _globals['_CHATRESPONSE']._serialized_end=564
  _globals['_ANALYSISREQUEST']._serialized_start=566
  _globals['_ANALYSISREQUEST']._serialized_end=629
  _globals['_ANALYSISRESPONSE']._serialized_start=631
  _globals['_ANALYSISRESPONSE']._serialized_end=707
  _globals['_ENDSESSIONREQUEST']._serialized_start=709
  _globals['_ENDSESSIONREQUEST']._serialized_end=748
  _globals['_ENDSESSIONRESPONSE']._serialized_start=750
  _globals['_ENDSESSIONRESPONSE']._serialized_end=810
  _globals['_LISTSESSIONSREQUEST']._serialized_start=812
  _globals['_LISTSESSIONSREQUEST']._serialized_end=833
  _globals['_LISTSESSIONSRESPONSE']._serialized_start=835
  _globals['_LISTSESSIONSRESPONSE']._serialized_end=878
  _globals['_CHARACTERCHATSERVICE']._serialized_start=881
  _globals['_CHARACTERCHATSERVICE']._serialized_end=1314
  _globals['_HEALTH']._serialized_start=1317
  _globals['_HEALTH']._serialized_end=1463
# @@protoc_insertion_point(module_scope)
