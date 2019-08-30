#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
from requests.sessions import RequestsCookieJar
from requests.compat import cookielib

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


def formart_selenium_cookies(cookies):
    cookie_dict = dict()
    for c in cookies:
        cookie_dict[c['name']] = c['value']
    return cookie_dict


def selenium_add_cookies(cookies, web, domain):
    cookie_list = [{'name': c[0], 'value': c[1], 'path': '/', 'domain': domain, 'expiry': 4070880000} for c in
                   cookies.items()]
    for c in cookie_list:
        web.add_cookie(c)


def cookiejar_from_dict(cookie_dict, domain, cookiejar=None, overwrite=True):
    """Returns a CookieJar from a key/value dictionary.

    :param cookie_dict: Dict of key/values to insert into CookieJar.
    :param cookiejar: (optional) A cookiejar to add the cookies to.
    :param overwrite: (optional) If False, will not replace cookies
        already in the jar with new ones.
    """
    if cookiejar is None:
        cookiejar = RequestsCookieJar()

    if cookie_dict is not None:
        names_from_jar = [cookie.name for cookie in cookiejar]
        for name in cookie_dict:
            if overwrite or (name not in names_from_jar):
                cookiejar.set_cookie(create_cookie(name, cookie_dict[name], domain))

    return cookiejar


def create_cookie(name, value, domain, **kwargs):
    """Make a cookie from underspecified parameters.

    By default, the pair of `name` and `value` will be set for the domain ''
    and sent on every request (this is sometimes called a "supercookie").
    """
    result = dict(
        version=0,
        name=name,
        value=value,
        port=None,
        domain=domain,
        path='/',
        secure=False,
        expires=None,
        discard=True,
        comment=None,
        comment_url=None,
        rest={'HttpOnly': None},
        rfc2109=False, )

    badargs = set(kwargs) - set(result)
    if badargs:
        err = 'create_cookie() got unexpected keyword arguments: %s'
        raise TypeError(err % list(badargs))

    result.update(kwargs)
    result['port_specified'] = bool(result['port'])
    result['domain_specified'] = bool(result['domain'])
    result['domain_initial_dot'] = result['domain'].startswith('.')
    result['path_specified'] = bool(result['path'])

    return cookielib.Cookie(**result)
