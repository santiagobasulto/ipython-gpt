from unittest.mock import MagicMock, patch

from ipython_gpt.api_client import OpenAIClient
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
        cmd.execute("", "Testing message")

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
        )
