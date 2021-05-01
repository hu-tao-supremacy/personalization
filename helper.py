from google.protobuf import wrappers_pb2 as wrapper
from google.protobuf.timestamp_pb2 import Timestamp

def getInt32Value(value):
    if value is None:
        return None
    temp = wrapper.Int32Value()
    temp.value = value
    return temp


def getStringValue(value):
    if value is None:
        return None
    temp = wrapper.StringValue()
    temp.value = value
    return temp

def getTimeStamp(data):
    if data is None:
        return None
    timestamp = Timestamp()
    timestamp.FromDatetime(data)
    return timestamp