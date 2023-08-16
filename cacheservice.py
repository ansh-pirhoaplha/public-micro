import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)
redis_client.setex(unique_id,60, str(latest_log))