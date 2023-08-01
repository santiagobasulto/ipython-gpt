# import http.client
import json
import urllib.parse
import requests 

OPEN_AI_API_HOST = "api.openai.com"
OPEN_AI_API_PORT = 443
DEFAULT_API_VERSION = "v1"


class APIClientException(Exception):
    pass


class APIResponseException(APIClientException):
    def __init__(self, method, path, response_status, response_body):
        self.method = method
        self.path = path
        self.response_status = response_status
        self.response_body = response_body

    def __str__(self):
        error_message = (
            (self.response_body or {})
            .get("error", {})
            .get("message", "No response from API.")
        )
        return f"Failed API Request '{self.method} {self.path}'. Got {self.response_status}: {error_message}"


class UnauthorizedAPIException(APIResponseException):
    pass


class OpenAIClient:
    def __init__(self, openai_api_key, api_version=DEFAULT_API_VERSION):
        self.openai_api_key = openai_api_key
        self.api_version = api_version

    def request(self, method, path, headers=None, query_params=None, json_body=None, stream=False):
        method = method.upper()
        assert path.startswith("/"), "Invalid path"
        assert not path.startswith(
            "/v"
        ), "API Version must be specified at moment of client creation"

        # connection = http.client.HTTPSConnection(
        #     host=OPEN_AI_API_HOST, port=OPEN_AI_API_PORT
        # )

        headers = headers or {}
        headers.setdefault("Authorization", f"Bearer {self.openai_api_key}")
        headers.setdefault("Content-Type", "application/json")

        body = None
        if json_body:
            body = json.dumps(json_body)

        url = f"https://{OPEN_AI_API_HOST}:{OPEN_AI_API_PORT}/{self.api_version}{path}"
        if query_params is not None:
            url += "?" + urllib.parse.urlencode(query_params)

        # connection.request(method, path, body, headers)
        resp = requests.request(method, url, headers=headers, data=body, stream=stream)
        # resp = connection.getresponse()
        if 200 <= resp.status_code < 300:
            if stream:
                resp_body = resp.read()
                print(resp_body.decode("utf-8"))
                pass # read using stream
                return resp.iter_lines()
            else:
                # TODO: this might raise an exception for an invalid body
                # content = json.loads(resp_body.decode("utf-8"))
                return resp.json()
        if resp.status_code == 401:
            raise UnauthorizedAPIException(method, path, resp.status_code, resp.json())

        # Catch all exception for any other not known status
        raise APIResponseException(method, path, resp.status_code, resp.json())
