!!This is still under construction (not yet on pip)!!

# Hooks

This package is made to provide a simple way to create hooks (callback) to common packages and functions.
Generally speaking, its relatively simple to create a hook, you import and attach to the process.

## Installation

There are multiple possible installations, depending on your need.

1. Simple install only the core hooks that do no require any dependencies:

    ```bash
    pip install common_hooks
    ```

1. Installing all (Not recommended):

    ```bash
    pip install common_hooks[all]
    ```

1. Installing only the hooks that require a specific package:

    ```bash
    pip install common_hooks[package_name]
    ```

1. You can install multiple hooks using comma separated list, for example:

    ```bash
    pip install common_hooks[httpx,fastapi]
    ```

## Available hooks include

- httpx
- fastapi

## Usage

To attach a callback function before all httpx GET calls:

```python
from common_hooks.httpx import hook
from common_hooks.conditions import HttpRequestCondition

complex_condition = HttpRequestCondition(methods=["GET"])
hook.attach(lambda _x: print(_x), mode="before", condition=complex_condition)
```

To attach a callback function after all httpx POST calls (after is default):

```python
from common_hooks.httpx import hook
from common_hooks.conditions import HttpRequestCondition

complex_condition = HttpRequestCondition(methods=["POST"])
hook.attach(lambda _x: print("Hello World!"), condition=complex_condition)
```

After attaching, you must install the hooks:

```python
hook.install()
```

To use multiple hooks in the same script rename them using "as":

```python
from common_hooks.conditions import HttpRequestCondition
from common_hooks.httpx import hook as httpx_hook
from common_hooks.fastapi import hook as fastapi_hook

complex_condition = HttpRequestCondition(methods=["POST"])

hook.attach(lambda _x: print("Hello World!"), condition=complex_condition)
httpx_hook.install()

fastapi_hook.attach(lambda _x: print("Hello World!"), condition=complex_condition)
fastapi_hook.install()
```

## Planned future hooks

-

## Possible future hooks

- aiohttp
- requests
- flask
- django

## Contribution

If you have a hook you would like to add, please create a pull request with the hook and a test to ensure it works as expected.
A hook must inherit from the CoreHook class you can import using:

```python
from common_hooks import CoreHook
```
