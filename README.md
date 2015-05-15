# adhipsta
adhipsta

## Prerequisites

1. Install Python 3.4 (or better)

2. Install `pip` tool (sometimes called `pyp3` to stress its for Python 3+)

3. Install npm

## Installing dependencies

Python dependencies:

```
pip install -r requirements.txt
```

Node dependencies:

```
npm install
```


## Running server

```
export PYTHONPATH=.
python adhipsta/server.py
```

## Configuring

All configurable pieces are in `adhipsta/config`


## Heroku deployment

Create an application named `adhipsta` on Heroku (using their web console)

Then tell Heroku to use multipack builder:
```
heroku config:add BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git -a adhipsta
```

Everything else is controlled by `Procfile`, `package.json`, `requirements.txt`, and `runtime.txt`

## Important environment variables
```
heroku config:add DOMAIN=http://adhipsta.herokuapp.com -a adhipsta
```
`DOMAIN` is needed for OAuth2 callback address. This is the name of the server running the application. Default is `http://localhost:9000`.

```
heroku config GOOGLE_ID=blah -a adhipsta
heroku config GOOGLE_SECRET=foo -a adhipsta
```
This is needed for Google OAuth2 login and adwords api token. Values are set in Google developers console for the AdHipsta application.
Make sure that AdHipsta Credentials are configured to accept correct callback address.
