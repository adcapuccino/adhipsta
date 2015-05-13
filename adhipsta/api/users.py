'''
Created on May 12, 2015

@author: mike
'''
import asyncio
from aiohttp import web
from adhipsta.util import Response
from adhipsta import auth_service
from asyncio_mongo._bson.objectid import ObjectId


def user_from_model(user):
    
    return {
        '_id'          : user.get('_id'),
        'name'         : user.get('name'),
        'email'        : user.get('email'),
        'role'         : user.get('role', 'user'),
        'provider'     : user.get('provider'),
        'has_api_token': user.get('api_token') is not None
    }


@asyncio.coroutine
def index(req):
    yield from auth_service.ensure_role(req, 'admin')

    db = req.app['mongo']
    
    user_records = yield from db.users.find()

    return Response.json([user_from_model(u) for u in user_records])


@asyncio.coroutine
def me(req):

    user = yield from auth_service.authenticated_user(req)

    return Response.json(user_from_model(user))
