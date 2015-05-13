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
    'name' : 'Development Tools',
    'info' : 'Integration with popular tools such as Bower, Grunt, Karma, Mocha, JSHint, Node Inspector, Livereload, Protractor, Jade, Stylus, Sass, CoffeeScript, and Less.'
  }, {
    'name' : 'Server and Client integration',
    'info' : 'Built with a powerful and fun stack: MongoDB, Express, AngularJS, and Node.'
  }, {
    'name' : 'Smart Build System',
    'info' : 'Build system ignores `spec` files, allowing you to keep tests alongside code. Automatic injection of scripts and styles into your index.html'
  },  {
    'name' : 'Modular Structure',
    'info' : 'Best practice client and server structures allow for more code reusability and maximum scalability'
  },  {
    'name' : 'Optimized Build',
    'info' : 'Build process packs up your templates as a single JavaScript payload, minifies your scripts/css/images, and rewrites asset names for caching.'
  },{
    'name' : 'Deployment Ready',
    'info' : 'Easily deploy your app to Heroku or Openshift with the heroku and openshift subgenerators'
  }
]

@asyncio.coroutine
def seed(db):
    yield from db.users.drop()
    yield from db.users.insert([auth_service.hashed_user(u) for u in USERS], safe=True)

    yield from db.things.drop()
    yield from db.things.insert(THINGS, safe=True)
