'''
Created on May 12, 2015

@author: mike
'''
from adhipsta.config import environment
from adhipsta.auth import oauth2
import asyncio
import datetime
from adhipsta import auth_service
from aiohttp import web


adwords_oauth = oauth2.OAuth2(
    'https://accounts.google.com/o/oauth2/auth',
    'https://accounts.google.com/o/oauth2/token',
    'https://accounts.google.com/o/oauth2/revoke',

    environment.Config.adwords['clientId'],
    environment.Config.adwords['clientSecret'],
    environment.Config.adwords['callbackUrl']
)


@asyncio.coroutine
def enter(req):
    user = yield from auth_service.authenticated_user(req)

    yield from adwords_oauth.enter(req, 
        access_type='offline',
        approval_prompt='force',
        scope='https://www.googleapis.com/auth/adwords',
        state=str(user['_id'])
    )


@asyncio.coroutine
def callback(req):
    user = yield from auth_service.authenticated_user(req)
    
    tokens = yield from adwords_oauth.callback(req)
    
    tokens['expires'] = (datetime.datetime.utcnow() + datetime.timedelta(seconds=1000 * int(tokens['expires_in']))).isoformat()

    user['api_token'] = tokens
    print('Obtained token:', tokens)
    
    mongo = req.app['mongo']
    yield from mongo.users.save(user)
    
    return web.HTTPFound('/settings')


@asyncio.coroutine
def release(req):
    user = yield from auth_service.authenticated_user(req)

    if user['api_token'] is not None:
        token = user['api_token']
        print('Revoking token:', token)
        token = token.get('refresh_token') or token.get('access_token')

        yield from adwords_oauth.release(token)
        
        user['api_token'] = None
        mongo = req.app['mongo']
        yield from mongo.users.save(user)

    return web.HTTPAccepted()
