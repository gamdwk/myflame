class Config(dict):
    debug = False
    database_uri = None
    host = None
    port = None
    secret_key = None
    session_life_time = None
    session_name = 'session'
    session_type = 'cookie'
    session_redis = None
    session_http_only = False

    def __getitem__(self, item):
        return getattr(self, item.lower())

    def __setitem__(self, key, value):
        setattr(self, key.lower(), value)

    def __delitem__(self, key):
        delattr(self, key.lower())

    def make_config(self, **kwargs):
        for key, value in kwargs.items():
            self[key] = value

    def from_map(self, mapping):
        for key, value in mapping.items():
            self[key] = value

    def from_object(self, config):
        for key in dir(config):
            if key.isupper():
                self[key] = getattr(config, key)
