import db

from flask import Flask, redirect, request, session
from tweepy.api import API
from tweepy.auth import OAuthHandler
from tweepy.error import TweepError

app = Flask(__name__)
app.secret_key = 'super secret key'

CALLBACK = 'http://localhost:5000/login/callback'

REQUEST_TOKEN_COOKIE = 'request_token'
TOKEN_SECRET_COOKIE = 'token_secret'
ACCESS_TOKEN_COOKIE = 'request_token'
ACCESS_TOKEN_SECRET_COOKIE = 'token_secret'

@app.route('/login/get-request-token')
def request_token():
    secrets = _get_twitter_secrets()
    if not secrets:
        return 'Could not load twitter secrets'

    auth = OAuthHandler(secrets['api_key'], secrets['secret'], CALLBACK)
    try:
        redirect_url = auth.get_authorization_url()
    except TweepError as e:
        return 'Error! Failed to get request token: %s' % e
    return redirect(redirect_url)

@app.route('/login/callback')
def access_token():
    secrets = _get_twitter_secrets()
    if not secrets:
        return 'Could not load twitter secrets'

    auth = OAuthHandler(secrets['api_key'], secrets['secret'], CALLBACK)
    request_token = request.args.get('oauth_token')
    verifier = request.args.get('oauth_verifier')
    auth.request_token = {
        'oauth_token' : request_token,
        'oauth_token_secret' : verifier
    }
    try:
        (access_token, access_token_secret) = auth.get_access_token(verifier)
    except TweepError as e:
        return 'Error! Failed to get access token: %s' % e
    session[ACCESS_TOKEN_COOKIE] = access_token
    session[ACCESS_TOKEN_SECRET_COOKIE] = access_token_secret
    api = API(auth)
    user_info = api.me()
    db.get_db().users.insert({
        'access_token' : access_token,
        'access_token_secret' : access_token_secret,
        'username' : user_info.screen_name,
    })
    return "logged in: %s" % access_token

@app.teardown_appcontext
def close(error):
    db.close_db()

def _is_logged_in():
    return session[ACCESS_TOKEN_COOKIE] and session[ACCESS_TOKEN_SECRET_COOKIE]

def _get_twitter_secrets():
    return db.get_db().secrets.find_one({'_id' : 'twitter'})
