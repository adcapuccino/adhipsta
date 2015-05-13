'''
Created on May 12, 2015

@author: mike
'''
import os
from adhipsta.api import things, users
from adhipsta.auth import local


def register(router):
    # things
    router.add_route('GET', '/api/things', things.index)

    # users
    router.add_route('GET', '/api/users/me', users.me)
    router.add_route('GET', '/api/users', users.index)
    
    # auth
    router.add_route('POST', '/auth/local', local.authenticate)
    
    router.add_static('/bower_components', os.path.join(os.path.dirname(__file__), '..', 'node_modules'))
    router.add_static('/', os.path.join(os.path.dirname(__file__), '..', 'client'))
    router.add_default(os.path.join(os.path.dirname(__file__), '..', 'client', 'index.html'))
