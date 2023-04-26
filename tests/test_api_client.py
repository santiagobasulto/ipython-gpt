import json
from http.client import HTTPSConnection
from unittest.mock import Mock, patch

from ipython_gpt.api_client import OpenAIClient


def test_api_client_auth():
    json_body = {"messages": [{"role": "user", "content": "Testing message"}]}

    with patch.object(HTTPSConnection, "request") as mocked_request:
        mock = Mock(status=200)
        mock.read.return_value = '{"choices": {"message": "Valid response"}}'.encode(
            "utf-8"
        )
        with patch.object(HTTPSConnection, "getresponse", return_value=mock):
            client = OpenAIClient("VERY SECRET KEY")
            client.request("POST", "/chat/completions", json_body=json_body)

            mocked_request.assert_called_once_with(
                "POST",
                "/v1/chat/completions",
                json.dumps(json_body),
                {
                    "Authorization": "Bearer VERY SECRET KEY",
                    "Content-Type": "application/json",
                },
            )
