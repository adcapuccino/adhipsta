'''
Created on May 12, 2015

@author: mike
'''
import asyncio
from adhipsta.util import Response


@asyncio.coroutine
def index(req):

    db = req.app['mongo']
    things = yield from db.things.find()

    return Response.json(things)
