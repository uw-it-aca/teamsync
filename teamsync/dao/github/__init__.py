from django.conf import settings
from restclients.dao import DAO_BASE
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import (
    get_mockdata_url, post_mockdata_url, delete_mockdata_url, put_mockdata_url)
from restclients.exceptions import DataFailureException
import json


class File(object):
    def getURL(self, url, headers):
        return get_mockdata_url('github', 'file', url, headers)

    def putURL(self, url, headers, body):
        return put_mockdata_url('github', 'file', url, headers, body)

    def postURL(self, url, headers, body):
        return post_mockdata_url('github', 'file', url, headers, body)

    def deleteURL(self, url, headers):
        return delete_mockdata_url('github', 'file', url, headers)


class Live(object):
    pool = None
    host = 'https://api.github.com'
    headers = {'Accept': 'application/vnd.github.v3+json',
               'User-Agent': 'uw-it-aca/teamsync',
               'Authorization': 'token %s' % getattr(
                   settings, 'RESTCLIENTS_GITHUB_OAUTH_TOKEN', '')}

    def getURL(self, url, headers):
        headers.update(Live.headers)
        return get_live_url(self._get_pool(), 'GET', Live.host, url,
                            headers=headers, service_name='github')

    def putURL(self, url, headers, body):
        headers.update(Live.headers)
        return get_live_url(self._get_pool(), 'PUT', Live.host, url,
                            headers=headers, body=body, service_name='github')

    def postURL(self, url, headers, body):
        headers.update(Live.headers)
        return get_live_url(self._get_pool(), 'POST', Live.host, url,
                            headers=headers, body=body, service_name='github')

    def deleteURL(self, url, headers):
        headers.update(Live.headers)
        return get_live_url(self._get_pool(), 'DELETE', Live.host, url,
                            headers=headers, service_name='github')

    def _get_pool(self):
        if Live.pool is None:
            Live.pool = get_con_pool(Live.host, verify_https=True,
                                     socket_timeout=15)
        return Live.pool


class GitHub_DAO(DAO_BASE):
    def getURL(self, url, headers={}):
        response = self._getDAO().getURL(url, headers)

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def putURL(self, url, headers={}, body={}):
        headers.update({'Content-Type': 'application/json'})
        response = self._getDAO().putURL(url, headers, json.dumps(body))

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def postURL(self, url, headers={}, body={}):
        headers.update({'Content-Type': 'application/json'})
        response = self._getDAO().postURL(url, headers, json.dumps(body))

        if response.status != 201:
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def deleteURL(self, url, headers={}):
        response = self._getDAO().deleteURL(url, headers)

        if response.status != 204:
            raise DataFailureException(url, response.status, response.data)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_GITHUB_DAO_CLASS', File)
