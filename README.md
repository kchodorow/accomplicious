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

## Running

```
bazel run //py
```
