'''
Created on May 12, 2015

@author: mike
'''
import asyncio
from aiohttp import web
from adhipsta.util import Response
from adhipsta import auth_service, jsonx


@asyncio.coroutine
def authenticate(req):
    params = yield from req.json()
    
    db = req.app['mongo']
    user = yield from db.users.find_one({'email': params['email'].lower()})
    if user is None:
        raise web.HTTPUnauthorized()
    
    if not auth_service.check_password(user, params['password']):
        raise web.HTTPUnauthorized()
    
    token = auth_service.sign_token(user['_id'], user['role'])

    return Response.json({'token': jsonx.dumps(token)})
