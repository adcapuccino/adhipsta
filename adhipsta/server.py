'''
Created on May 12, 2015

@author: mike
'''
import asyncio
import aiohttp.web as web
import logging
from adhipsta import routes
import asyncio_mongo
from adhipsta.config import environment
from adhipsta.seed import seed
from adhipsta.aiohttp_util.urldispatcher import UrlDispatcher


logging.basicConfig(level=logging.DEBUG)

@asyncio.coroutine
def mongodb(config):
    conn = yield from asyncio_mongo.Pool.create(url=config.mongo['url'])
    return getattr(conn, config.mongo['db'])

@asyncio.coroutine
def logging_middleware(app, handler):
    
    @asyncio.coroutine
    def h(req):
        logging.debug('%s %s %r' % (req.method, req.path_qs, req.headers))
        return (yield from handler(req))

    return h

@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop, router=UrlDispatcher(), middlewares=[logging_middleware])
    routes.register(app.router)

    mongo = yield from mongodb(environment.Config)

    app['mongo'] = mongo

    if environment.Config.seedDb:
        yield from seed(mongo)

    server = yield from loop.create_server(app.make_handler(), '0.0.0.0', environment.Config.port)
    print('Server started on 0.0.0.0:9000')
    return server

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
