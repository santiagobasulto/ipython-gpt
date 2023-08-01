import json
import requests
from unittest.mock import Mock, patch

from ipython_gpt.api_client import OPEN_AI_API_HOST, OPEN_AI_API_PORT, OpenAIClient


def test_api_client_auth():
    json_body = {"messages": [{"role": "user", "content": "Testing message"}]}

    with patch.object(requests, "request") as mocked_request:
        mocked_response = Mock(status_code=200)
        mocked_response.json.return_value = {"choices": {"message": "Valid response"}}
        mocked_request.return_value = mocked_response
        client = OpenAIClient("VERY SECRET KEY")
        client.request("POST", "/chat/completions", json_body=json_body, stream=False)
        url =  f"https://{OPEN_AI_API_HOST}:{OPEN_AI_API_PORT}/v1/chat/completions"
        mocked_request.assert_called_once_with(
            "POST",
            url,
            headers={
                "Authorization": "Bearer VERY SECRET KEY",
                "Content-Type": "application/json",
            },
            data=json.dumps(json_body),
            stream=False
        )
