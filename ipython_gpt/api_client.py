import http.client
import json
import urllib.parse

OPEN_AI_API_HOST = "api.openai.com"
OPEN_AI_API_PORT = 443
DEFAULT_API_VERSION = "v1"


class APIClientException(Exception):
    pass


class APIResponseException(APIClientException):
    def __init__(self, method, path, headers, query_params, body):
        self.method = method
        self.path = path
        self.headers = headers
        self.query_params = query_params
        self.body = body

    def __str__(self):
        return f"Failed API Request '{self.method} {self.path}'"


class OpenAIClient:
    def __init__(self, openai_api_key, api_version=DEFAULT_API_VERSION):
        self.openai_api_key = openai_api_key
        self.api_version = api_version

    def request(self, method, path, headers=None, query_params=None, json_body=None):
        method = method.upper()
        assert path.startswith("/"), "Invalid path"
        assert not path.startswith(
            "/v"
        ), "API Version must be specified at moment of client creation"

        connection = http.client.HTTPSConnection(
            host=OPEN_AI_API_HOST, port=OPEN_AI_API_PORT
        )

        headers = headers or {}
        headers.setdefault("Authorization", f"Bearer {self.openai_api_key}")
        headers.setdefault("Content-Type", "application/json")

        body = None
        if json_body:
            body = json.dumps(json_body)

        path = f"/{self.api_version}" + path
        if query_params is not None:
            path += "?" + urllib.parse.urlencode(query_params)

        try:
            connection.request(method, path, body, headers)
            resp = connection.getresponse()

            if 200 <= resp.status < 300:
                resp_body = resp.read()
                if resp_body and len(resp_body) > 0:
                    return json.loads(resp_body.decode("utf-8"))
            else:
                raise APIResponseException(method, path, headers, query_params, body)
        finally:
            connection.close()
