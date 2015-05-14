'''
Created on May 12, 2015

@author: mike
'''
import asyncio
from adhipsta.auth import oauth2
from adhipsta.config import environment
from adhipsta.util import Response
from aiohttp import web
from adhipsta import auth_service
import json


google_oauth = oauth2.OAuth2(
    'https://accounts.google.com/o/oauth2/auth',
    'https://accounts.google.com/o/oauth2/token',
    environment.Config.google['clientId'],
    environment.Config.google['clientSecret'],
    environment.Config.google['callbackUrl'],
    scope = [
      'https://www.googleapis.com/auth/userinfo.profile',
      'https://www.googleapis.com/auth/userinfo.email'
    ]
)


@asyncio.coroutine
def enter(req):
    yield from google_oauth.enter(req)


@asyncio.coroutine
def callback(req):
    tokens = yield from google_oauth.callback(req)
    
    accessToken = tokens['access_token']
    profile = yield from google_oauth.get('https://www.googleapis.com/plus/v1/people/me', accessToken)

    # normalize profile
    user = {
        'provider': 'google',
        'role'    : 'user',
        'name'    : profile['displayName'],
        'email'   : profile['emails'][0]['value'],
        'google'  : {
            'id': profile['id'],
        }
    }

    mongo = req.app['mongo']

    yield from mongo.users.insert([user])
    user = yield from mongo.users.find_one(user)

    jwt_token = auth_service.sign_token(user['_id'], user['role'])

    response = web.HTTPFound('/')
    response.set_cookie('token', json.dumps(jwt_token))
    raise response
