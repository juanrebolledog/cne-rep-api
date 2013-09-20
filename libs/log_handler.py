import os


class CustomFileHandler(object):

    def __init__(self, dir, logger, handlerFactory, **kw):
        kw['filename'] = os.path.join(dir, logger.name)
        self._handler = handlerFactory(**kw)

    def __getattr__(self, n):
        if hasattr(self._handler, n):
            return getattr(self._handler, n)
        raise AttributeError, n