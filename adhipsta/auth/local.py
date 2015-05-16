'''
Created on May 12, 2015

@author: mike
'''
import asyncio
from aiohttp import web
from adhipsta import auth_service, util


@asyncio.coroutine
def authenticate(req):
    params = yield from req.json()
    
    db = req.app['mongo']
    user = yield from db.users.find_one({'email': params['email'].lower()})
    if user is None:
        raise web.HTTPUnauthorized()
    
    if not auth_service.check_password(user, params['password']):
        raise web.HTTPUnauthorized()
    
    jwt_token = auth_service.sign_token(user['_id'], user['role'])
    
    response = web.HTTPAccepted()
    response.set_cookie('token', util.Angular.serialize_cookie(jwt_token))
    raise response
