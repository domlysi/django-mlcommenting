# Imports the Google Cloud client library
import os

from ipware import get_client_ip
from py_translator import Translator

import django_mlcommenting


def google_translate(text, target='en'):
    if not target:
        target = 'en'
    # Instantiates a client
    translator = Translator()
    try:
        new = translator.translate(text, dest=target)
    except AttributeError as e:
        print(e)
        return None
    if new.extra_data['confidence'] and float(new.extra_data['confidence']) > float(0.8) and new.text != text:
        return new
    return None


def get_cc(ip):
    import pygeoip
    geoip_dat = os.path.join(os.path.dirname(django_mlcommenting.__file__), 'files', 'geoip', 'GeoIP.dat')
    gi = pygeoip.GeoIP(geoip_dat)
    if not gi:
        return None
    return str(gi.country_code_by_addr(ip))


def get_ip(request):
    client_ip, is_routable = get_client_ip(request)
    if client_ip is None:
        return None
    # Unable to get the client's IP address
    else:
        # We got the client's IP address
        if is_routable:
            # The client's IP address is publicly routable on the Internet
            pass
        else:
            # The client's IP address is private
            pass
    return client_ip
    # Order of precedence is (Public, Private, Loopback, None)


def get_comment_relative_width(comments):
    ratings = {
        5: {
            'value': comments.filter(rating=5).count(),
            'width': None
        },
        4: {
            'value': comments.filter(rating=4).count(),
            'width': None
        },
        3: {
            'value': comments.filter(rating=3).count(),
            'width': None
        },
        2: {
            'value': comments.filter(rating=2).count(),
            'width': None
        },
        1: {
            'value': comments.filter(rating=1).count(),
            'width': None
        }
    }
    ratings_values = []
    for i in range(1, len(ratings) + 1):
        ratings_values.append(ratings[i]['value'])

    if max(ratings_values) == 0:
        return ratings
    factor = float(100 / float(max(ratings_values)))
    for i in range(1, len(ratings) + 1):
        ratings[i]['width'] = ratings[i]['value'] * factor
    return ratings
