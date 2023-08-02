from unittest.mock import MagicMock, patch

from ipython_gpt.api_client import IPythonGPTResponse, OpenAIClient
from ipython_gpt.subcommands import ChatCommand


def test_basic_chat_command():
    SYSTEM_MESSAGE = "You're a python data science coding assistant"
    GPT_MODEL = "gpt-3.5-turbo"
    with patch.object(OpenAIClient, "request", MagicMock()) as mocked_request:
        context = {
            "config": {
                "openai_api_key": "VERY SECRET KEY",
                "default_model": GPT_MODEL,
                "default_system_message": SYSTEM_MESSAGE,
            },
            "message_history": [],
        }
        cmd = ChatCommand(context)
        resp = cmd.execute("", "Testing message")
        for r in resp:
            assert r.is_streaming == False

        mocked_request.assert_called_once_with(
            "POST",
            "/chat/completions",
            json_body={
                "model": GPT_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_MESSAGE},
                    {"role": "user", "content": "Testing message"},
                ],
            },
            stream=False,
        )

def test_streaming_chat_command():
    SYSTEM_MESSAGE = "You're a python data science coding assistant"
    GPT_MODEL = "gpt-3.5-turbo"
    side_effects = [
        IPythonGPTResponse({"choices": [{"delta": {"content": "foo"}}]}, True),
        IPythonGPTResponse({"choices": [{"delta": {"content": "bar"}}]}, True)
    ]
    with patch.object(OpenAIClient, "request", MagicMock()) as mocked_request:
        mocked_request.return_value = side_effects
        context = {
            "config": {
                "openai_api_key": "VERY SECRET KEY",
                "default_model": GPT_MODEL,
                "default_system_message": SYSTEM_MESSAGE,
            },
            "message_history": [],
        }
        cmd = ChatCommand(context)
        resp = cmd.execute("--stream", "Testing message")
        returned_data = [r for r in resp]
        assert returned_data == ["foo", "bar"]   

        # Message history must not be for the conatenation of all stream messages.
        assert cmd.context["message_history"][-1]["content"]== "foobar"

        mocked_request.assert_called_once_with(
            "POST",
            "/chat/completions",
            json_body={
                "model": GPT_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_MESSAGE},
                    {"role": "user", "content": "Testing message"},
                ],
            },
            stream=True,
        )