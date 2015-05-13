'''
Created on May 12, 2015

@author: mike
'''
import os


class ConfigBase:
    ''' environment type: development or production '''
    env = os.environ.get('NODE_ENV', 'development')

    ''' server root '''
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

    ''' server port '''
    port = int(os.environ.get('PORT', '9000'))
    
    mongo = {
        'url': 'mongodb://dev:dev@ds031822.mongolab.com:31822/dev',
        'db' : 'dev'
    }

    # do we need to populate default db
    seedDb = False
    
    secret = {
        # secret phrase for JWT encryption/decryption
        'jwt': 'adhipsta big secret'
    }

    google = {
        'clientID'    : os.environ.get('GOOGLE_ID', 'id'),
        'clientSecret': os.environ.get('GOOGLE_SECRET', 'secret'),
        'callbackURL' : os.environ.get('DOMAIN', '') + '/auth/google/callback'
    }
    
    adwords = {
        'clientID'    : os.environ.get('ADHIPSTA_ID', '650003686975-c2kikodb6dc8190so8oh83bbvr7s260h.apps.googleusercontent.com'),
        'clientSecret': os.environ.get('ADHIPSTA_SECRET', 'ACblH6zl_6MY8diWlgjcyZua'),
        'callbackURL' : os.environ.get('DOMAIN', '') + '/auth/adwords/callback'
    }

if ConfigBase.env == 'development':
    from adhipsta.config import development
    Config = development.Config
elif ConfigBase.env == 'production':
    from adhipsta.config import production
    Config = production.Config
else:
    raise RuntimeError('unknown server environment ' + repr(ConfigBase.env))
