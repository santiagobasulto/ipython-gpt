import argparse
import shlex

from .api_client import OpenAIClient


class BaseIPythonGPTCommand:
    def __init__(self, context):
        self.context = context
        self._openai_api_key = None

    def _customize_parser(self, parser):
        return parser

    def _execute(self, client, args, line, cell):
        raise NotImplementedError

    def build_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--openai-api-key",
            help="The OpenAI API Key to use. Can be also set as envvars",
        )
        parser.add_argument(
            "--reset-conversation",
            help="Start a brand new conversation without previous context",
            action="store_true",
        )
        parser.add_argument(
            "--system-message",
            help="The initial system message used to start the conversation. Use `--no-system-message` to skip it.",
        )
        parser.add_argument(
            "--model",
            help="The OpenAI model to use. Use `%chat_models` to display the available ones",
        )
        return self._customize_parser(parser)

    def parse_args(self, line):
        parser = self.build_parser()
        return parser.parse_args(shlex.split(line))

    def execute(self, line, cell=None):
        args = self.parse_args(line)
        # TODO: Add logging (and new argument --debug)
        # if debug: logger.log()

        # TODO: Look for a way to refactor args and config. Smells
        openai_api_key = args.openai_api_key or self.context["config"]["openai_api_key"]
        assert bool(openai_api_key), "OPENAI_API_KEY missing"
        client = OpenAIClient(openai_api_key)
        results = self._execute(client, args, line, cell)
        return results


class ChatCommand(BaseIPythonGPTCommand):
    COMMAND_NAME = "chat"

    def _customize_parser(self, parser):
        parser.add_argument(
            "--no-system-message",
            help="Avoid passing an initial message or role to the assistant",
            action="store_true",
        )
        parser.add_argument(
            "--temperature",
            help="What sampling temperature to use, between 0 and 2. See OpenAI docs",
            type=float,
        )
        parser.add_argument(
            "--max-tokens",
            help="The maximum number of tokens to generate in the chat completion.",
            type=int,
        )
        return parser

    def _execute(self, client, args, line, cell=None):
        message_history = self.context["message_history"]
        if args.reset_conversation:
            message_history = []

        system_message = (
            args.system_message or self.context["config"]["default_system_message"]
        )

        if len(message_history) == 0:
            message_history = [
                {"role": "system", "content": system_message},
            ]
        messages = message_history + [{"role": "user", "content": cell}]

        model = args.model or self.context["config"]["default_model"]
        json_body = {"model": model, "messages": messages}

        if args.temperature:
            json_body["temperature"] = args.temperature
        if args.max_tokens:
            json_body["max_tokens"] = args.max_tokens

        resp = client.request("POST", "/chat/completions", json_body=json_body)
        chat_response = resp["choices"][0]["message"]["content"]
        message_history += [
            {"role": "assistant", "content": chat_response},
        ]
        self.context["message_history"] = message_history
        return chat_response


class ConfigCommand(BaseIPythonGPTCommand):
    def _execute(self, client, args, line, cell=None):
        if args.openai_api_key:
            self.context["config"]["openai_api_key"] = args.openai_api_key
        if args.model:
            self.context["config"]["default_model"] = args.model

        if args.system_message:
            self.context["config"]["default_system_message"] = args.system_message

        if args.reset_conversation:
            self.context["message_history"] = []

        response = f"""
##### Conf set:

* **Default model**: {self.context['config']['default_model']}
* **Default system message**: {self.context['config']['default_system_message']}
* **Chat history length**: {len(self.context['message_history'])}
"""
        return response


class ChatModelsBrowserCommand(BaseIPythonGPTCommand):
    def _customize_parser(self, parser):
        parser.add_argument(
            "--all-models",
            help="Display all the available models, not just ChatGPT ones",
            action="store_true",
        )
        return parser

    def _execute(self, client, args, line, cell):
        resp = client.request("GET", "/models")
        models = [
            m["id"]
            for m in resp["data"]
            if args.all_models or m["id"].startswith("gpt")
        ]
        formatted_models = "\n".join([f"\t- {model}" for model in models])
        return f"##### Available models:\n\n{formatted_models}"
