'''
Created on May 12, 2015

@author: mike
'''
import asyncio
from adhipsta import auth_service


USERS = [
  {
    'provider': 'local',
    'name': 'Test User',
    'email': 'test@test.com',
    'password': 'test'
  }, {
    'provider': 'local',
    'role': 'admin',
    'name': 'Erik Nijkamp',
    'email': 'erik@erik.com',
    'password': 'erik'
  }, {
    'provider': 'local',
    'role': 'admin',
    'name': 'Mike Kroutikov',
    'email': 'mike@mike.com',
    'password': 'mike'
  }
]

THINGS = [
  {
    'name' : 'Easy setup',
    'info' : 'No-fuzz easy-to-follow setup wizard. Start your advertising campaign in 5 minutes or less.'
  }, {
    'name' : 'Beautiful reports',
    'info' : 'Keep an eye on performance - reports in PDF/HTML format generated automatically and delivered to you.'
  }, {
    'name' : 'Deep optimization',
    'info' : 'Performs over 20 optimizations to ensure the highest bang for your money.'
  },  {
    'name' : 'Autopilot included',
    'info' : 'As advertising market drifts our unique Autopilot feature takes necessary steps to keep performance high.'
  },  {
    'name' : 'Learns on-the-go',
    'info' : 'Learns seasonal, weekly, and daily patterns and uses them to deliver more with less.'
  },{
    'name' : 'Straightforward pricing',
    'info' : 'No upfront fees, no hidden fees. Easy and transparent subscription pricing, starting at $10/month'
  }
]

@asyncio.coroutine
def seed(db):
    yield from db.users.drop()
    yield from db.users.insert([auth_service.hashed_user(u) for u in USERS], safe=True)

    yield from db.things.drop()
    yield from db.things.insert(THINGS, safe=True)
