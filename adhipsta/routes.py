'''
Created on May 12, 2015

@author: mike
'''
import os
from adhipsta.api import things, users
from adhipsta.auth import local, google, adwords


def register(router):
    # things
    router.add_route('GET', '/api/things', things.index)

    # users
    router.add_route('GET', '/api/users/me', users.me)
    router.add_route('GET', '/api/users', users.index)
    
    # auth/local
    router.add_route('POST', '/auth/local', local.authenticate)

    # auth/google
    router.add_route('GET', '/auth/google/callback', google.callback)
    router.add_route('GET', '/auth/google', google.enter)
    
    # auth/adwortds api
    router.add_route('GET', '/auth/adwords/callback', adwords.callback)
    router.add_route('DELETE', '/auth/adwords/api_token', adwords.release)
    router.add_route('GET', '/auth/adwords', adwords.enter)
    
    router.add_static('/bower_components', os.path.join(os.path.dirname(__file__), '..', 'node_modules'))
    router.add_static('/', os.path.join(os.path.dirname(__file__), '..', 'client'))
    router.add_default(os.path.join(os.path.dirname(__file__), '..', 'client', 'index.html'))
