import os
import shlex
import argparse
import requests

import IPython as ipy
from IPython.display import display, HTML, Markdown
from IPython.core.magic import Magics, magics_class, cell_magic, line_magic

DISPLAY_METHODS = {
    "ZMQInteractiveShell": "display_notebook",
    "TerminalInteractiveShell": "display_shell"
}

parser = argparse.ArgumentParser()

parser.add_argument("--openai-api-key", help="The OpenAI API Key to use. Can be also set as envvars")
parser.add_argument(
    "--reset-conversation", help="Start a brand new conversation without previous context",
    action="store_true")
parser.add_argument(
    "--system-message", help="The initial system message used to start the conversation. Use `--no-system-message` to skip it.")
parser.add_argument(
    "--no-system-message", help="Avoid passing an initial message or role to the assistant",
    action="store_true")
parser.add_argument("--model", help="The OpenAI model to use. Use `%chat_models` to display the available ones")
parser.add_argument("--temperature", help="What sampling temperature to use, between 0 and 2. See OpenAI docs", type=float)
parser.add_argument("--max-tokens", help="The maximum number of tokens to generate in the chat completion.", type=int)
parser.add_argument("--all-models", help="Display all the available models, not just ChatGPT ones", action="store_true")


@magics_class
class IPythonGPT(Magics):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.openai_api_key = os.environ.get("OPENAI_API_KEY") or globals().get("OPENAI_API_KEY")

        self.default_model = "gpt-3.5-turbo"
        self.default_system_message = "You're a python data science coding assistant"

        self.message_history = []

    def display_notebook(self, message):
        display(Markdown(message))

    def display_shell(self, message):
        display(message)

    def display(self, message):
        method_name = DISPLAY_METHODS.get(
            ipy.get_ipython().__class__.__name__, "display_shell")
        getattr(self, method_name)(message)

    @cell_magic
    def chat(self, line, cell):
        assert bool(cell.strip()), "Content of cell can't be empty, check usage"

        args = parser.parse_args(shlex.split(line))
        openai_api_key = args.openai_api_key or self.openai_api_key
        assert bool(openai_api_key), "OPENAI_API_KEY missing"

        if args.reset_conversation:
            self.message_history = []

        system_message = args.system_message or self.default_system_message

        if len(self.message_history) == 0:
            self.message_history = [
                {"role": "system", "content": system_message},
            ]
        messages = self.message_history + [{"role": "user", "content": cell}]

        model = args.model or self.default_model
        json_body = {
            "model": model,
            "messages": messages
        }
        if args.temperature:
            json_body['temperature'] = args.temperature
        if args.max_tokens:
            json_body['max_tokens'] = args.temperature
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openai_api_key}",
            }, json=json_body)

        resp.raise_for_status()
        chat_response = resp.json()['choices'][0]['message']['content']
        self.message_history += [
            {"role": "user", "content": cell},
            {"role": "assistant", "content": chat_response},

        ]
        self.display(chat_response)

    @line_magic
    def chat_config(self, line):
        args = parser.parse_args(shlex.split(line))
        openai_api_key = args.openai_api_key or self.openai_api_key
        assert bool(openai_api_key), "OPENAI_API_KEY missing"

        if args.openai_api_key:
            self.openai_api_key = args.openai_api_key
        if args.model:
            self.default_model = args.model

        if args.system_message:
            self.default_system_message = args.system_message

        if args.reset_conversation:
            self.message_history = []

        response = f"""
##### Conf set:

* **Default model**: {self.default_model}
* **Default system message**: {self.default_system_message}
* **Chat history length**: {len(self.message_history)}
"""
        self.display(response.strip())

    @line_magic
    def chat_help(self, line):
        parser.print_usage()

    @line_magic
    def chat_models(self, line):
        args = parser.parse_args(shlex.split(line))
        openai_api_key = args.openai_api_key or self.openai_api_key
        assert bool(openai_api_key), "OPENAI_API_KEY missing"

        resp = requests.get(
            "https://api.openai.com/v1/models",
            headers={
                "Authorization": f"Bearer {self.openai_api_key}",
            })
        resp.raise_for_status()
        models = [m['id'] for m in resp.json()['data'] if args.all_models or m['id'].startswith('gpt')]
        formatted_models = "\n".join([f"\t- {model}" for model in models])
        self.display(f"##### Available models:\n\n{formatted_models}")


name = "ipython_gpt"

def load_ipython_extension(ipython):
    ipython.register_magics(IPythonGPT)
