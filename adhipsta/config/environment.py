'''
Created on May 12, 2015

@author: mike
'''
import os
import codecs


'''
If ~/.adhipsta exists, read environment vars from there
'''
_rcfile = os.path.expanduser(r'~/.adhipsta')
if os.path.isfile(_rcfile):
    with codecs.open(_rcfile, 'r', 'utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            env_name, env_value = line.split('=', 2)
            os.environ[env_name.strip()] = env_value.strip()


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
        'jwt': 'adhipsta big secret',
        
        # how many days login token is valid (will force re-login is expired)
        'jwt_expiration_days': 14
    }

    google = {
        'clientId'    : os.environ.get('GOOGLE_ID', 'id'),
        'clientSecret': os.environ.get('GOOGLE_SECRET', 'secret'),
        'callbackUrl' : os.environ.get('DOMAIN', 'http://localhost:9000') + '/auth/google/callback'
    }
    
    adwords = {
        'clientId'    : os.environ.get('ADWORDS_ID', 'id'),
        'clientSecret': os.environ.get('ADWORDS_SECRET', 'secret'),
        'callbackUrl' : os.environ.get('DOMAIN', 'http://localhost:9000') + '/auth/adwords/callback'
    }

if ConfigBase.env == 'development':
    from adhipsta.config import development
    Config = development.Config
elif ConfigBase.env == 'production':
    from adhipsta.config import production
    Config = production.Config
else:
    raise RuntimeError('unknown server environment ' + repr(ConfigBase.env))
