import urllib
from time import time
import hashlib
import hmac
import base64
import random
import re


def normalize_data(http_method, request_url, params):
    '''
    Create data to calculate signature
    :param http_method str: http method string
    :param request_url str: http request url
    :param params dict: params of http header
    :rtype: str
    :return: data string for calculate oauth1.0 signature
    '''
    pattern = '(\\?).*'
    identify = re.search(pattern, str(request_url))
    if(identify != None):
        query_params = identify.group(0)
        Qparams = str(query_params).replace('?','')
        newURL = str(request_url).replace(identify.group(0),'')
        conversion_params = ({x.split('=')[0]:str(x.split('=')[1]) for x in Qparams.split("&")})
        params.update(conversion_params) 

        query_str = '&'.join(['='.join([key, urllib.quote(params.get(key, ''
                         ), '')]) for key in sorted(params.keys())])
        return '&'.join([urllib.quote(val, '') for val in
                        [http_method.upper(), newURL,query_str]
                        if val is not None])
    else:
        query_str = '&'.join(['='.join([key, urllib.quote(params.get(key, ''
                             ), '')]) for key in sorted(params.keys())])
        return '&'.join([urllib.quote(val, '') for val in
                        [http_method.upper(), request_url, query_str]
                        if val is not None])


def normalize_key(consumer_secret, resource_owner_secret=None):
    '''
    Create key to calculate signature

    :param consumer_secret str:
    :param resource_owner_secret str:
    :rtype: str
    :return: key string for calculate oauth1.0 signature
    '''

    return '&'.join([urllib.quote(key, '') for key in [consumer_secret,
                    resource_owner_secret or '']])


def make_signature(normalized_key, normalized_data):
    '''
    Create signature
    :param normalized_key str:
    :param normalized_data str:
    :rtype: str
    :return: Calculated signature
    '''

    signature = hmac.new(bytes(normalized_key).encode('utf-8'),
                         bytes(normalized_data).encode('utf-8'),
                         hashlib.sha1)
    return base64.b64encode(signature.digest()).decode('utf-8')


def prepare_token(
    url,
    method,
    key,
    secret,
    ):
    consumer_key = key
    consumer_key_secret = secret

    nonce = str(random.randrange(000000000000000000000000000000,
                999999999999999999999999999999, 30))
    timestr = str(int(time()))
    pattern = ':\\d+?/'
    identify = re.search(pattern, str(url))
    raw_url = \
        str(url).replace(identify.group(0),
                         '/')
    request_url = str(raw_url).strip()
    http_method = str(method).strip()

    oauth_params = {
        'oauth_consumer_key': consumer_key,
        'oauth_nonce': nonce,
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': timestr,
        'oauth_version': '1.0',
        }

    q_params = {}
    [q_params.update({k: v}) for (k, v) in oauth_params.items()
     if k.startswith('oauth') if v is not None]

    n_key = normalize_key(consumer_key_secret)
    n_data = normalize_data(http_method, request_url, q_params)
    signature = make_signature(n_key, n_data)
    header = 'Authorization: OAuth '
    for (k, v) in oauth_params.items():
        header += str(k) + '="' + str(v) + '",'
    header += 'oauth_signature="' + signature + '"'
    return header
