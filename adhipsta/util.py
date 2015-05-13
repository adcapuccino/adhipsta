'''
Created on May 12, 2015

@author: mike
'''
from adhipsta import jsonx
from aiohttp import web


class Response:
    
    @classmethod
    def json(cls, obj):
        res = web.Response(body=jsonx.dumps(obj).encode('utf-8'))
        res.content_type = 'application/json'
        return res
