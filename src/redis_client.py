import redis
import pickle


class RedisClient:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self.redis = redis.Redis(host=host, port=port, db=db)

    def save_data(self, data: dict):
        try:
            serialized_data = pickle.dumps(data)
            self.redis.set('claim_experiences', serialized_data)
        finally:
            self.redis.close()

    def __del__(self):
        if hasattr(self, 'redis') and self.redis:
            self.redis.close()