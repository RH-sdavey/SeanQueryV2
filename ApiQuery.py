import requests
from urllib3.exceptions import MaxRetryError

from ApiResponse import APIResponse


class DiagnosticAnalyticsServiceApi(object):
    """Object that is able to get a token to interact with an API, and send simple get request to an API endpoint"""

    def __init__(self):
        self._headers = None
        self._TOKEN_URL = 'Token URL here'
        self._API_ENDPOINT = "API Endpoint URL here"

    def get_auth_token(self, user, pwd):
        """Retrieve an API token
        This token may be used to send requests to the REST API

        The token returned is a str(json) object that contains a few fields,
        this method extracts and returns just the access_token in a str() format.

        If no valid token object is returned from the token api, then a False value will be returned and the test suite
        setup should fail based on that.

        :param str user: the user to create a token for
        :param str pwd: the password for the user to create a token for
        :return: this method finished successfully, valid v3 access token which may be used to access the IOTA API
        :rtype: tuple(bool, str)
        """
        try:
            token_obj = requests.post(
                url=self._TOKEN_URL,
                data={
                    "grant_type": "password",
                    "username": user,
                    "password": pwd,
                    "scope": "o",
                    "client_id": "blaj",
                    "client_secret": ""
                }
            )
        except requests.ConnectionError as e:
            return False, "No token retrieved, ConnectionErrorException was caught: " + e.message

        if not token_obj:
            return False, "An invalid token was returned by the Token server, possibly empty. Check manually."
        return True, str(token_obj.json()['access_token'])

    def query_real_time_usage_endpoint(self, dimension, token):
        """send GET request to an API endpoint, with param:dimension and param:token
        The response is wrapped in a ApiResponse object, which can be used to parse the return values easily.

        ./ApiResponse.py
        for more information

        :param str dimension: api dimension and parameter values
        :param str token: token to validate the requests authentication to the server
        :return: Object that allows for easy parsing of response data/values
        :rtype: tuple(bool, ApiResponse)
        """
        url = f"{self._API_ENDPOINT}/{dimension}"

        self._headers = {
            'Accept-Version': "0.0.1",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + token,
        }
        try:
            r = requests.get(
                url=url,
                headers=self._headers,
            )
            return True, APIResponse(r)
        except requests.ConnectionError as e:
            return False, "GET request to API, ConnectionErrorException was caught: " + e.message
        except MaxRetryError as e:
            return False, "GET request to API, MaxRetryError was caught: " + e.message
