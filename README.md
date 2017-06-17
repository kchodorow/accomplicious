# Accomplogi

Emogi-based accomplishment tracker.

## Prerequisites:

```
pip install virtualenv Flask tweepy pymongo emoji
virtualenv venv
```

Run MongoDB.  I've been running a local instance pointed to a db directory for
dev:

```
mkdir db
mongod --dbpath db
```

Then add Twitter secrets:

```
use accomploji
API_KEY = '<API KEY>'
SECRET = '<SECRET>'
db.secrets.insert({_id : 'twitter', api_key : API_KEY, secret : SECRET})
```

## Running

```
bazel run //py
```

The web app uses Bootstrap & D3 from CDNs, so the HTML won't look right offline.
