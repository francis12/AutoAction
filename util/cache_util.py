import os, json


class CacheUtil:

    # Cache = []
    Cache = {}
    @classmethod
    def load_cache_from_file(cls, file='cache'):
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                file = f.read()
            cls.Cache = json.loads(file)

    @classmethod
    def flush_cache_file(cls, file='cache'):
        json_str = json.dumps(cls.Cache)
        cache_file = open(file, 'w', encoding='utf-8')
        cache_file.write(json_str)
        cache_file.close()
