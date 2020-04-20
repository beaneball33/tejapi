import re

import requests

from .util import Util
from .version import VERSION
from .api_config import ApiConfig
from tejapi.errors.tej_error import (
    TejError, LimitExceededError, InternalServerError,
    AuthenticationError, ForbiddenError, InvalidRequestError,
    NotFoundError, ServiceUnavailableError)

class Connection:
    @classmethod
    def request(cls, http_verb, url, **options):
        if 'headers' in options:
            headers = options['headers']
        else:
            headers = {}

        accept_value = 'application/json'
        if ApiConfig.api_version:
            accept_value += ", application/vnd.tej+json;version=%s" % ApiConfig.api_version

        headers = Util.merge_to_dicts({'accept': accept_value,
                                       'request-source': 'python',
                                       'request-source-version': VERSION}, headers)
        if http_verb=='post':
            headers = Util.merge_to_dicts({'Content-Type':'application/x-www-form-urlencoded'}, headers)
            
        if ApiConfig.api_key:
            headers = Util.merge_to_dicts({'x-api-token': ApiConfig.api_key}, headers)

        options['headers'] = headers

        abs_url = '%s/%s' % (ApiConfig.api_base, url)

        return cls.execute_request(http_verb, abs_url, **options)

    @classmethod
    def execute_request(cls, http_verb, url, **options):
        try:
            #print(options)
            #print(url)
            func = getattr(requests, http_verb)
            response = func(url, **options)
            
            if response.status_code < 200 or response.status_code >= 300:
                cls.handle_api_error(response)
            else:
                return response
        except requests.exceptions.RequestException as e:
            if e.response:
                cls.handle_api_error(e.response)
            raise e

    @classmethod
    def parse(cls, response):
        try:
            return response.json()
        except ValueError:
            raise TejError(http_status=response.status_code, http_body=response.text)

    @classmethod
    def handle_api_error(cls, resp):
        error_body = cls.parse(resp)
        # if our app does not form a proper tej_error response
        # throw generic error
        if 'error' not in error_body:
            raise TejError(http_status=resp.status_code, http_body=resp.text)

        code = error_body['error']['code']
        message = error_body['error']['message']
        prog = re.compile('^([a-zA-Z])')
        if prog.match(code):
            code_letter = prog.match(code).group(1)
        
        d_klass = {
            'L': LimitExceededError,
            'M': InternalServerError,
            'A': AuthenticationError,
            'P': ForbiddenError,
            'S': InvalidRequestError,
            'C': NotFoundError,
            'X': ServiceUnavailableError
        }

        klass = d_klass.get(code_letter, TejError)

        raise klass(message, resp.status_code, resp.text, resp.headers, code)
