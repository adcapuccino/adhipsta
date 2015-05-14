'''
Created on May 12, 2015

@author: mike
'''
import asyncio
import urllib
from aiohttp import web, client
import logging
import code
from adhipsta.util import Response


class OAuth2:

    def __init__(self, authorizationUrl, tokenUrl, clientId, clientSecret, callbackUrl, scope=None):
        self._authorizationUrl = authorizationUrl
        self._tokenUrl = tokenUrl
        self._clientId = clientId
        self._clientSecret = clientSecret
        self._callbackUrl = callbackUrl
        self._scope = scope

    @asyncio.coroutine
    def enter(self, req):
        params = {
            'response_type': 'code',
            'redirect_uri' : self._callbackUrl,
            'client_id'    : self._clientId
        }

        if self._scope:
            if type(self._scope) is str:
                params['scope'] = self._scope
            else:
                # assume it a list of strings
                params['scope'] = ' '.join(self._scope)

        location = self._authorizationUrl + '?' + urllib.parse.urlencode(params)
        raise web.HTTPFound(location)

    @asyncio.coroutine
    def callback(self, req):
        query = urllib.parse.parse_qs(req.query_string) if req.query_string else {}

        if query.get('error'):
            logging.debug('Oauth2 error:', query['error'])
            raise web.HTTPUnauthorized()
        
        if query.get('code'):
            code = query['code']
            return (yield from self.getAccessTokens(code, grant_type='authorization_code', redirect_uri=self._callbackUrl))

        raise web.HTTPUnauthorized()
    
    @asyncio.coroutine
    def getAccessTokens(self, code, grant_type='refresh_token', **kw):
        params = {
            'grant_type'   : grant_type,
            #'redirect_uri' : self._callbackUrl,
            'client_id'    : self._clientId,
            'client_secret': self._clientSecret
        }
        
        params.update(kw)
        
        if grant_type == 'refresh_token':
            params['refresh_token'] = code
        else:
            params['code'] = code

        r = yield from client.request('post', self._tokenUrl, data=params)
        if r.status != 200:
            raise RuntimeError('bad token?')
        result = yield from r.json()
        return result

    @asyncio.coroutine
    def get(self, url, accessToken):
        r = yield from client.request('get', url, params={'access_token': accessToken})
        return (yield from r.json())

