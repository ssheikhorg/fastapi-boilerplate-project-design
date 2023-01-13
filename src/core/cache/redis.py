from dramatiq.brokers.redis import RedisBroker
from redis import from_url


"""Redis Cloud Connection"""
data = dict(
    host="localhost",
    port=14227,
    username="default",
    password="default"
)
redis = from_url(url=f"redis://{data['username']}:{data['password']}@{data['host']}:{data['port']}", decode_responses=True)


redis_broker = RedisBroker(url=f"redis://{data['username']}:{data['password']}@{data['host']}:{data['port']}")
