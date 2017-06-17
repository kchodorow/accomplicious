import db

from flask import session


USERNAME_COOKIE = 'username'
ACCESS_TOKEN_COOKIE = 'access_token'
ACCESS_TOKEN_SECRET_COOKIE = 'token_secret'

def is_same(target_user):
    """Checks that the logged in user is the same user as target_user."""
    if not is_logged_in():
        return False
    return target_user['access_token'] == session[ACCESS_TOKEN_COOKIE] \
        and target_user['access_token_secret'] == session[ACCESS_TOKEN_SECRET_COOKIE]

def is_logged_in():
    """Checks if someone, anyone, is logged in."""
    if not USERNAME_COOKIE in session:
        return False
    user = db.get_db().users.find_one({'_id' : session[USERNAME_COOKIE]})
    if not user:
        unset()
        return False
    if not ACCESS_TOKEN_COOKIE in session \
       or not ACCESS_TOKEN_SECRET_COOKIE in session:
        return False
    return user['access_token'] == session[ACCESS_TOKEN_COOKIE] \
        and user['access_token_secret'] == session[ACCESS_TOKEN_SECRET_COOKIE]


def set_access_token(username, access_token, access_token_secret):
    session[USERNAME_COOKIE] = username
    session[ACCESS_TOKEN_COOKIE] = access_token
    session[ACCESS_TOKEN_SECRET_COOKIE] = access_token_secret

def unset():
    session.pop(USERNAME_COOKIE, None)
    session.pop(ACCESS_TOKEN_COOKIE, None)
    session.pop(ACCESS_TOKEN_SECRET_COOKIE, None)
