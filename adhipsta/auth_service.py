'''
Created on May 12, 2015

@author: mike
'''
from aiohttp import web
import jwt
from adhipsta.config import environment
import asyncio
import uuid
import hashlib
from asyncio_mongo._bson.objectid import ObjectId
from aiohttp.web_exceptions import HTTPUnauthorized
import datetime
from adhipsta import util


@asyncio.coroutine
def authenticated_user(req):

    token = req.cookies.get('token')
    if token is None:
        raise web.HTTPUnauthorized()
    
    token = util.Angular.deserialize_cookie(token)
    
    try:
        user = jwt.decode(token, environment.Config.secret['jwt'])
    except:
        raise web.HTTPUnauthorized()

    db = req.app['mongo']

    user_record = yield from db.users.find_one({'_id' : ObjectId(user['_id'])})
    if user_record is None or user_record.get('_id') is None:
        raise web.HTTPUnauthorized()

    return user_record


@asyncio.coroutine
def ensure_role(req, role):
    '''
    role can be either a single role (a string) or a set of acceptable roles
    '''

    user = yield from authenticated_user(req)

    if type(role) == str and user.get('role') != role:
        raise HTTPUnauthorized()

    if user.get('role') not in role:
        raise HTTPUnauthorized()

def hash_password(password, salt=None):
    if salt is None:
        salt = uuid.uuid4().hex
    return hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest(), salt


def hashed_user(user):
    
    hashedPassword, salt = hash_password(user['password'])
    return {
        'provider': user.get('provider'),
        'name'    : user.get('name'),
        'email'   : user.get('email'),
        'role'    : user.get('role', 'user'),
        'salt'    : salt,
        'hashedPassword': hashedPassword
    }


def check_password(user, password):
    hashedPassword, _ = hash_password(password, user['salt'])
    
    return user['hashedPassword'] == hashedPassword


def sign_token(_id, role):
    return jwt.encode({
        '_id' : str(_id), 
        'role': role,
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=environment.Config.secret['jwt_expiration_days'])
    }, environment.Config.secret['jwt']).decode('ascii')

