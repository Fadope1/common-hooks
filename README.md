!!This is still under construction (not yet on pip)!!

# Hooks

This package is made to provide a simple way to create hooks (callback) to common packages and functions.
Generally speaking, its relatively simple to create a hook, you import and attach to the process.

## Installation

There are multiple possible installations, depending on your need.

1. Simple install only the core hooks that do no require any dependencies:

    ```bash
    pip install default_hooks
    ```

1. Installing all (Not recommended):

    ```bash
    pip install default_hooks[all]
    ```

1. Installing only the hooks that require a specific package:

    ```bash
    pip install default_hooks[package_name]
    ```

1. You can install multiple hooks using comma separated list, for example:

    ```bash
    pip install default_hooks[httpx,fastapi]
    ```

## Available hooks include

- httpx
- fastapi

## Usage

To attach a callback function before all httpx GET calls that have "/v1" in the url:

```python
from default_hooks.httpx import hook
hook.attach(("GET", "/v1", "before"), lambda: print("Hello World!"))
```

To attach a callback function after all httpx POST calls (after is default):

```python
from default_hooks.httpx import hook
hook.attach("POST", lambda: print("Hello World!"))
```

To attach a callback function before all httpx POST calls:

```python
from default_hooks.httpx import hook
hook.attach(("POST", "", "before"), lambda: print("Hello World!"))
```

Attaching a callback function does not apply the changes directly, instead you must apply the attachments:

```python
hook.apply()
```

To use multiple hooks in the same script rename them using "as":

```python
from default_hooks.httpx import hook as httpx_hook
from default_hooks.fastapi import hook as fastapi_hook

httpx_hook.attach("GET", lambda: print("Hello World!")) # prints "Hello World!" before all httpx GET calls
httpx_hook.apply()

fastapi_hook.attach("GET", lambda: print("Hello World!")) # prints "Hello World!" before endpoint is executed
fastapi_hook.apply()
```

## Planned future hooks

- none

## Possible future hooks

- aiohttp
- requests
- flask
- django

## Contribution

If you have a hook you would like to add, please create a pull request with the hook and a test to ensure it works as expected.
A hook must inherit from the CoreHook class you can import using:

```python
from default_hooks import CoreHook
```
