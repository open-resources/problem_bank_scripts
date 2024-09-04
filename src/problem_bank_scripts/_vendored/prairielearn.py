def __getattr__(name: str):
    return lambda *args, **kwargs: None