# Accomplogi

Emogi-based accomplishment tracker.

## Prerequisites:

Run MongoDB.  I've been running a local instance pointed to a db directory for
dev:

```
mkdir db
mongod --dbpath db
```

Create a `.env` file with the following content:

```
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=testdb
TWITTER_API_KEY=...
TWITTER_API_SECRET=...
```

## Test

```
heroku local
```

## Deploy

```
git push heroku
```
