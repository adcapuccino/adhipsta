'''
Created on May 12, 2015

@author: mike
'''
import asyncio
import urllib
from aiohttp import web, client
import logging
import code


class OAuth2:

    def __init__(self, authorizationUrl, tokenUrl, revokeUrl, clientId, clientSecret, callbackUrl):
        self.authorizationUrl = authorizationUrl
        self.tokenUrl = tokenUrl
        self.revokeUrl = revokeUrl
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.callbackUrl = callbackUrl

    @asyncio.coroutine
    def enter(self, req, scope, **options):
        params = {
            'response_type': 'code',
            'redirect_uri' : self.callbackUrl,
            'client_id'    : self.clientId
        }

        if type(scope) is list:
            params['scope'] = ' '.join(scope)
        else:
            params['scope'] = str(scope)

        for name, value in options.items():
            params[name] = str(value)

        location = self.authorizationUrl + '?' + urllib.parse.urlencode(params)
        raise web.HTTPFound(location)

    @asyncio.coroutine
    def callback(self, req, **options):
        query = urllib.parse.parse_qs(req.query_string) if req.query_string else {}

        if query.get('error'):
            logging.debug('Oauth2 error: %s', query['error'])
            raise web.HTTPUnauthorized()
        
        if query.get('code'):
            code = query['code']
            return (yield from self.getAccessTokens(code, grant_type='authorization_code', **options))

        raise web.HTTPUnauthorized()

    @asyncio.coroutine
    def getAccessTokens(self, code, grant_type='refresh_token', **options):
        params = {
            'grant_type'   : grant_type,
            'redirect_uri' : self.callbackUrl,
            'client_id'    : self.clientId,
            'client_secret': self.clientSecret
        }
        
        params.update(options)
        
        if grant_type == 'refresh_token':
            params['refresh_token'] = code
        else:
            params['code'] = code

        r = yield from client.request('post', self.tokenUrl, data=params)
        if r.status != 200:
            raise RuntimeError('bad token?')
        
        return (yield from r.json())

    @asyncio.coroutine
    def release(self, token):
        if token is None:
            raise RuntimeError('trying to release empty token')

        r = yield from client.request('get', self.revokeUrl, params={'token': token})
        if r.status != 200:
            raise RuntimeError('attempt to release token failed')
