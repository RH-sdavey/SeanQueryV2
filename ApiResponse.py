from typing import Any


class APIResponse(object):
    """
    Object representing a REST API Response. Methods and attributes here will allow the developer/user of the REST API
    to easily parse and test elements of the response (status_code and object body)
    """
    def __init__(self, response):
        self.response = Any()
        self.status_code = int()
        self.state = bool()
        self.flat_response = dict()
        self.response_json = dict()
        self.headers = dict()

        self.parse_response_object(response)

        if self.response_json.get('access_token', False):                     # Authorization Token Response
            self.token = self.response_json['access_token']
        else:
            self.flat_response = self.flatten_response(self.response.json())  # API Response

    def parse_response_object(self, response):
        """Parses the param:response and sets class level attributes from the key/value pairs

        :return:
        :rtype:
        """
        self.response = response
        self.response_json = self.response.json()
        self.state = self.response.ok
        self.status_code = self.response.status_code
        self.headers = self.response.headers

    @staticmethod
    def flatten_response(response):
        """Flatten json object with nested keys into a single level list.

        Json objects can be deeply nested kay/value pairs that also contain lists as values, because of that in can be
        difficult to access and parse the exact key needed sometimes.
        This method creates a list with all key/value pairs on one level, robot can then be used to access the list
        element, check if an element exists ... etc)

        Tip: in robot tests you can execute
        Log to Console    ${api_response.flat_response}
        to see the results of this method.

        :return: a flattened json object
        :rtype: dict
        """
        out = {}

        def flatten(x, name=''):
            """A nested method which will recursively traverse through a json object"""

            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '.')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '.')
                    i += 1
            else:
                out[name[:-1]] = x
        flatten(response)
        return out
