'''
Created on May 12, 2015

@author: mike
'''
from adhipsta import jsonx
from aiohttp import web
import urllib


class Response:
    
    @classmethod
    def json(cls, obj):
        res = web.Response(body=jsonx.dumps(obj).encode('utf-8'))
        res.content_type = 'application/json'
        return res


class Angular:
    '''
    Angular expects json-serialized objects in its $cookieStore. When server pushes a cookie to the
    client it must follow angular convention, otherwise client will see weird errors and exceptions
    because apparently angular parses all values it finds in the cookie store.
    '''
    
    @classmethod
    def serialize_cookie(cls, obj):
        return urllib.parse.quote(jsonx.dumps(obj))
    
    @classmethod
    def deserialize_cookie(cls, s):
        return jsonx.loads(urllib.parse.unquote(s))
