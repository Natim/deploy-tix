"""This module enables CRUD operations with Bugzilla 5.1 REST API

.. _Bugzilla REST API Docs:
   https://wiki.mozilla.org/Bugzilla:REST_API
   http://bugzilla.readthedocs.org/en/latest/api/index.html
"""

import sys
import json
import requests

from deploy_tix.output_helper import OutputHelper

URL_BUGZILLA_PROD = 'https://bugzilla.mozilla.com'
URL_BUGZILLA_DEV = 'https://bugzilla-dev.allizom.org'
# LINE = '------------------'

class InvalidCredentials(Exception):
    pass

class BugzillaRESTAPI(object):
    """"Used for CRUD operations against Bugzilla REST API

    Currently only supports authentication and create NEW.
    TODO: add bug update

    Use against URL_BUGZILLA_DEV to test.
    """

    def __init__(self, host, bugzilla_username, bugzilla_password):

        self.output = OutputHelper()
        self.host = host
        self.username = bugzilla_username
        self.password = bugzilla_password
        self.token = self.get_token(host)


    def get_json(self, release_num, product, environment, status, description):
        """Create bugzilla JSON to POST to REST API.

        Returns:
            JSON string
        """

        data = {
            'product':'Mozilla Services',
            'component':'General',
            'version':'unspecified',
            'op_sys':'All',
            'rep_platform':'All'
        }
        short_desc = 'Please deploy {} {} to {}'.format(
            release_num, product, environment)
        data.update(
            {'short_desc': short_desc,
             'description': description, 'status': status}
        )
        return data


    # TODO(rpapa): it would save authentication time to cache token for re-use
    #              add a try / except & query a new one if expired
    def get_token(self, host):
        """Fetch and return bugzilla token.

        Returns:
            string token
        """

        url = '{}/rest/login?login={}&password={}'.format(
            host, self.username, self.password)
        req = requests.get(url)
        decoded = json.loads(req.text)
        try:
            if 'token' not in decoded:
                raise InvalidCredentials
        except InvalidCredentials:
            err_header = self.output.get_header('BUGZILLA ERROR')

            err_msg = '{}\n{}\n{}\n\n'.format(
            err_header,
            decoded['message'],
            decoded['documentation'])

            sys.exit(err_msg)
        else:
            return decoded['token']


    def create_bug(
            self, release_num, product, environment, status, description):
        """Create bugzilla bug with description

        Note:
            On bugzilla-dev - available status:
            UNCONFIRMED, NEW, ASSIGNED, RESOLVED

        Returns:
            json string to POST to REST API
        """

        url = '{}/rest/bug?token={}'.format(self.host, self.token)
        req = requests.post(url)
        data = self.get_json(
            release_num, product, environment, status, description)
        print data

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        req = requests.post(url, data=json.dumps(data), headers=headers)
        print 'CREATE BUG: {}'.format(req.status_code)
        return req.text

def main():

    bugzilla_username = 'johnnyquest@racebannon.com'
    bugzilla_password = 'hadji_is_a_geek'
    ticket = BugzillaRESTAPI(
        URL_BUGZILLA_DEV, bugzilla_username, bugzilla_password)

    bug_info = {'release_num': '1.2.3',
                'product': 'demo-server',
                'environment': 'STAGE',
                'status': 'NEW',
                'description': 'Lorem ipsum dolor sit amet, \
                ne dicat ancillae...'}

    print ticket.create_bug(**bug_info)


if __name__ == '__main__':

    main()



