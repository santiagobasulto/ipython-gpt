import json
import requests
from unittest.mock import Mock, patch

from ipython_gpt.api_client import OPEN_AI_API_HOST, OPEN_AI_API_PORT, IPythonGPTResponse, OpenAIClient


def test_api_client_auth():
    json_body = {"messages": [{"role": "user", "content": "Testing message"}]}

    with patch.object(requests, "request") as mocked_request:
        mocked_response = Mock(status_code=200)
        mocked_response.json.return_value = {"choices": {"message": "Valid response"}}
        mocked_request.return_value = mocked_response
        client = OpenAIClient("VERY SECRET KEY")
        response = client.request("POST", "/chat/completions", json_body=json_body, stream=False)

        for r in response: # Consume the generator
            assert isinstance(r, IPythonGPTResponse)
            assert r.is_streaming == False

        url =  f"https://{OPEN_AI_API_HOST}:{OPEN_AI_API_PORT}/v1/chat/completions"
        mocked_request.assert_called_once_with(
            "POST",
            url,
            # "/v1/chat/completions",
            headers={
                "Authorization": "Bearer VERY SECRET KEY",
                "Content-Type": "application/json",
            },
            data=json.dumps(json_body),
            stream=False
        )

def test_api_client_streaming():
    """
    curl https://api.openai.com/v1/chat/completions -u :$OPENAI_API_KEY  -H 'Content-Type: application/json' -d '{"stream": true,"model": "gpt-3.5-turbo-0613", "messages": [ {"role": "user", "content": "Summarize Othello by Shaekspeare in a few lines?"}]}
    """
    json_body = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hi can you summarize 4 different most popular python PEPs in a few sentences each?"}],
        "stream": True,
    }

    with patch.object(requests, "request") as mocked_request:
        mocked_response = Mock(status_code=200, headers={"Content-Type": "text/event-stream"})
        mock_responses = [
            {"id":"foo","object":"chat.completion.chunk","created":1690924386,"model":"gpt-3.5-turbo-0613","choices":[{"index" :0,"delta":{"content":" deceit"},"finish_reason":None}]},
            {"id":"bar","object":"chat.completion.chunk","created":1690924386,"model":"gpt-3.5-turbo-0613","choices":[{"index" :0,"delta":{"content":"."},"finish_reason":None}]},              
            {"id":"bam","object":"chat.completion.chunk","created":1690924386,"model":"gpt-3.5-turbo-0613","choices":[{"index" :0,"delta":{},"finish_reason":"stop"}]}
        ]
        mock_data = [('data: '+json.dumps(i)).encode() for i in mock_responses]
        mock_data.append('data: [DONE]'.encode())                                                                                                                                                                                
        mocked_response.iter_lines.return_value = mock_data

        mocked_request.return_value = mocked_response
        client = OpenAIClient("VERY SECRET KEY")
        response = client.request("POST", "/chat/completions", json_body=json_body, stream=True)
        for i, r in enumerate(response): # Consume the generator
            assert isinstance(r, IPythonGPTResponse)
            assert r.is_streaming == True 
            assert r.data == mock_responses[i]

        url =  f"https://{OPEN_AI_API_HOST}:{OPEN_AI_API_PORT}/v1/chat/completions"
        mocked_request.assert_called_once_with(
            "POST",
            url,
            headers={
                "Authorization": "Bearer VERY SECRET KEY",
                "Content-Type": "application/json",
            },
            data=json.dumps(json_body),
            stream=True
        )
