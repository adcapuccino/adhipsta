'''
Created on May 26, 2015

@author: mike
'''
import asyncio
from adhipsta import auth_service
from adhipsta.util import Response
from aiohttp import web
from dateutil import parser as date_parser
from googleads.adwords import AdWordsClient
from adhipsta.config import environment
from googleads.oauth2 import GoogleRefreshTokenClient
import urllib


def strip_slashes(x):
    if x and x[0] == '/':
        x = x[1:]
    if x and x[-1] == '/':
        x = x[:-1]
    return x


def join_path(*av):
    av = [strip_slashes(x) for x in av]
    av = [x for x in av if x]
    
    return '/' + '/'.join(av)


def mount_as(router, mount_point):
    router.add_route('GET', join_path(mount_point, 'campaigns'), index)



def adwords_client_from_api_token(api_token):
    developer_token = environment.Config.developer_token
    oauth2_client = GoogleRefreshTokenClient(
        client_id=environment.Config.adwords['clientId'],
        client_secret=environment.Config.adwords['clientSecret'],
        refresh_token=api_token['refresh_token']
    ) 

    oauth2_client.oauth2credentials.token_expiry = date_parser.parse(api_token['expires'])
    oauth2_client.oauth2credentials.access_token = api_token['access_token']

    return AdWordsClient(developer_token=developer_token, 
                  oauth2_client=oauth2_client,
                  user_agent='AdHipsta',
                  client_customer_id=environment.Config.client_customer_id)


@asyncio.coroutine
def index(req):
    user = yield from auth_service.authenticated_user(req)
    
    api_token = user.get('api_token')
    if api_token is None:
        raise web.HTTPNotFound()

    client = adwords_client_from_api_token(user['api_token'])
    campaign_service = client.GetService('CampaignService', version='v201502')

    query = urllib.parse.parse_qs(req.query_string) if req.query_string else {}
    offset = int(query.get('offset', '0'))
    page_size = int(query.get('page_size', '100'))

    # Construct selector and get all campaigns.
    selector = {
        'fields': ['Id', 'Name', 'Status'],
        'paging': {
            'startIndex': str(offset),
            'numberResults': str(page_size)
        }
    }

    page = campaign_service.get(selector)
    entries = page['entries'] if 'entries' in page else []

    return Response.json([{'name': e['name'], 'id': e['id'], 'status': e['status']} for e in entries])
