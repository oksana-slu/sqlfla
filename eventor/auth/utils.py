from flask import session


def login(user):
    session['uid'] = user.id


def logout():
    session.pop('uid')
