from django.conf import settings
from restclients_core.dao import DAO


class GitHub_DAO(DAO):
    def service_name(self):
        return 'github'

    def _custom_headers(self, method, url, headers, body):
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'uw-it-aca/teamsync',
            'Authorization': 'token %s' % getattr(
                settings, 'RESTCLIENTS_GITHUB_OAUTH_TOKEN', '')
        }

        if "POST" == method or "PUT" == method:
            headers.update({'Content-Type': 'application/json'})

        return headers
