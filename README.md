# IPython ChatGPT extension

[![Black badge](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![prettier badge](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?logo=prettier&logoColor=white)](https://github.com/prettier/prettier)
[![pre-commit](https://img.shields.io/badge/pre--commit-active-yellow?logo=pre-commit&logoColor=white)](https://pre-commit.com/)4
[![test](https://img.shields.io/github/actions/workflow/status/santiagobasulto/ipython-gpt/test.yaml?logo=github&logoColor=white)](https://github.com/santiagobasulto/ipython-gpt/actions/workflows/test.yaml)

This extension allows you to use ChatGPT directly from your Jupyter Notebook or IPython Shell ([Demo](https://github.com/santiagobasulto/ipython-gpt/blob/master/Demo.ipynb)).

<img width="900" alt="IPython GPT, a Jupyter/IPython interface for Chat GPT" src="https://user-images.githubusercontent.com/872296/232230454-44529ea4-920e-4294-9d61-550771a4a95e.png">

<img width="900" alt="IPython GPT, a Jupyter/IPython interface for Chat GPT" src="https://user-images.githubusercontent.com/872296/232230492-9bc50342-9d78-4adb-8168-2f94fcbc3b73.png">

**Important!** This is a very early and raw version, I have a lot of things to improve regarding code quality and missing functionality. Check [this issue](https://github.com/santiagobasulto/ipython-gpt/issues/4) for a rough "roadmap".

## Installation

```python
!pip install ipython-gpt
```

Then in your notebook or ipython shell:

```ipython
%load_ext ipython_gpt
```

## Setup

You must first generate an API key at OpenAI (https://platform.openai.com/account/api-keys) and set is an environment variable `OPENAI_API_KEY`. You can do it by modifying your `.bashrc/.zshrc` or starting jupyter with it:

```bash
$ OPENAI_API_KEY=[YOUR-KEY] jupyter lab
# ...
$ OPENAI_API_KEY=[YOUR-KEY] ipython
```

There are a few other ways to set the API KEY, but the envvar is the recommended one.

## ChatGPT API

The command `%%chat` interfaces with ChatGPT. It accepts multiple parameters (see Usage). Here's an example:

```python
%%chat --max-tokens=25

What's the purpose of life?
...

>>> CHAT RESPONSE
```

**Important** by default, the `%%chat` command preserves the conversation to give the Agent some context, in the same way that ChatGPT works. You can "reset" its status passing the flag `--reset-conversation`.

```python
%%chat --reset-conversation

How can I avoid pandas using scientific notation in outputs, and do it globally?
...
...
>>> CHAT RESPONSE
```

## Agent's role (system message) and other chat parameters

By default, the Chat is started with the role: _"You're a python data science coding assistant"_. You can change that by passing something different in your first `%%chat`:

```ipython
%%chat --system-message="You're a R Data Science assistant"

Your message...
```

Once the conversation has started, you can't change the original message, as the context is preserved. To do so, you must reset the conversation:

```ipython
%%chat --system-message="You're a R Data Science assistant" --reset-conversation

Your message...
```

## Setting global config

You can change the defaults using the `%chat_config` line magic:

```ipython
%chat_config --system-message="You're an R data scientist coding assistant specialized in visualizations" --model "other model" --reset-conversation
```

Invoke it without parameters to see the defaults set:

```python
%chat_config
...

>>>
##### Conf set:

* **Default model**: gpt-3.5-turbo
* **Default system message**: You're a python data science coding assistant
* **Chat history length**: 0
```

## Other methods

#### Display available models

Usage:

```bash
%chat_models [--all-models]
```

```python
%chat_models
```

##### Available models:

    - gpt-3.5-turbo-0301
    - gpt-3.5-turbo

#### Display usage and accepted parameters

```python
%reload_ext ipython_gpt
%chat_help
...


    usage: ipykernel_launcher.py [-h] [--openai-api-key OPENAI_API_KEY]
                                 [--reset-conversation]
                                 [--system-message SYSTEM_MESSAGE]
                                 [--no-system-message] [--model MODEL]
                                 [--temperature TEMPERATURE]
                                 [--max-tokens MAX_TOKENS] [--all-models]

```

## Alternative authentication

Aside from setting the environment variable, you can also set `OPENAI_API_KEY` as a global variable in your notebook, or pass it directly as a parameter in any method `--openai-api-key=YOUR-KEY`.

These alternative methods are NOT recommended, as you might leak your API Key in the notebooks' history, stored in `.ipynb_checkpoints`.
