import Cookie
import os
import requests


def get_cookies():
    s = requests.session()
    r = s.get("http://www.twitter.com")

    cookie =  r.cookies['_twitter_sess']

    return cookie
