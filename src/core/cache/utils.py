import json

from src import serializers


class RedisDataSerializer:
    @classmethod
    def dumps(cls, data):
        return json.dumps(data, cls=serializers.Encoder)

    @classmethod
    def loads(cls, data):
        return json.loads(data)
