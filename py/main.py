import accomplish
import datetime
import db
import json
import pymongo
import user_helpers

from flask import Flask, make_response, redirect, request, send_from_directory, session, url_for
from tweepy.api import API
from tweepy.auth import OAuthHandler
from tweepy.error import TweepError
from bson.objectid import ObjectId

app = Flask(__name__)
# This is required for Flask to work.
app.secret_key = 'super secret key'

REQUEST_TOKEN_COOKIE = 'request_token'

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/user.html')
def user():
    return app.send_static_file('user.html')

@app.route('/js/<path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/assets/<path>')
def send_assets(path):
    return send_from_directory('static/assets', path)

@app.route('/app/login/get-request-token')
def request_token():
    if user_helpers.is_logged_in():
        response = make_response('Already logged in!')
        user_helpers.setup_user(response)
        return response
    secrets = _get_twitter_secrets()
    if not secrets:
        return 'Could not load twitter secrets'

    auth = OAuthHandler(secrets['api_key'], secrets['secret'])
    try:
        redirect_url = auth.get_authorization_url()
    except TweepError as e:
        return 'Error! Failed to get request token: %s' % e
    if not auth.request_token['oauth_callback_confirmed']:
        return 'OAuth callback unconfirmed?'
    session[REQUEST_TOKEN_COOKIE] = auth.request_token['oauth_token']
    return redirect(redirect_url)

@app.route('/app/login/callback')
def access_token():
    if user_helpers.is_logged_in():
        response = make_response('Already logged in!')
        user_helpers.setup_user(response)
        return response
    if not REQUEST_TOKEN_COOKIE in session:
        return 'Request token not set'
    secrets = _get_twitter_secrets()
    if not secrets:
        return 'Could not load twitter secrets'

    auth = OAuthHandler(secrets['api_key'], secrets['secret'])
    request_token = request.args.get('oauth_token')
    # request_token should match the token stored in request_token().
    if request_token != session[REQUEST_TOKEN_COOKIE]:
        return '%s did not match request token (%s)' % (
            request_token, session[REQUEST_TOKEN_COOKIE])
    verifier = request.args.get('oauth_verifier')
    auth.request_token = {
        'oauth_token' : request_token,
        'oauth_token_secret' : verifier
    }
    try:
        (access_token, access_token_secret) = auth.get_access_token(verifier)
    except TweepError as e:
        return 'Error! Failed to get access token: %s' % e

    api = API(auth)
    user_info = api.me()
    username = user_info.screen_name
    response = make_response('Logged in: %s' % access_token)
    user_helpers.set_access_token(username, access_token, access_token_secret, response)
    db.get_db().users.update({
        '_id' : username,
    }, {
        '$set' : {
            'access_token' : access_token,
            'access_token_secret' : access_token_secret
        },
    }, upsert = True)
    return response

@app.route('/app/logout')
def logout():
    response = make_response('Logged out')
    user_helpers.unset(response)
    session.pop(REQUEST_TOKEN_COOKIE, None)
    return response

@app.route('/app/done', methods=['POST'])
def done():
    if not user_helpers.is_logged_in():
        return redirect('/app/login/get-request-token')
    accomplishment = accomplish.parse(request.form['accomplishment'])
    accomplishment['user'] = session[user_helpers.USERNAME_COOKIE]
    accomplishment['created'] = datetime.datetime.now()
    accomplishment['public'] = False
    db.get_db().accomplishments.insert(accomplishment)
    return redirect('/')

@app.route('/app/api/a/<aid>')
def a(aid):
    a = db.get_db().accomplishments.find_one({'_id' : ObjectId(aid)})
    if not a:
        return '{}'
    if a['public']:
        return json.dumps(a)
    # Accomplishment exists but is private, check if the target user is the
    # logged-in user.
    target_user = db.get_db().users.find_one({'_id' : a['user']})
    if user_helpers.is_same(target_user):
        return json.dumps(a)
    return '{}'

@app.route('/app/api/timeline/<username>')
def timeline(username):
    query = {'user' : username}
    target_user = db.get_db().users.find_one({'_id' : username})
    if not user_helpers.is_same(target_user):
        app.logger.warning('public only: %s' % session)
        query['public'] = True
    cursor = db.get_db().accomplishments.find(query).limit(100).sort(
        'created', pymongo.DESCENDING
    )
    entries = []
    for doc in cursor:
        entries.append({
            'a' : doc['a'],
            'created' : doc['created'].strftime('%I:%M%p %B %d, %Y'),
        })
    return json.dumps(entries)

@app.teardown_appcontext
def close(error):
    db.close_db()

def _get_twitter_secrets():
    return db.get_db().secrets.find_one({'_id' : 'twitter'})
