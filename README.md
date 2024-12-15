# Common-hooks

This package is made to provide a simple way to create hooks (callback) to common packages and functions.
Generally speaking, its relatively simple to create a hook, you import and attach to the process.

## Next steps
[x] Create basic tests
[ ] Upload to pypi
[ ] Advanced test support
[ ] Integrate requests library
[ ] Integrate aiohttp library

## Installation (not yet working)

There are multiple possible installations, depending on your need.

1. Simple install only the core hooks that do no require any dependencies (which is currently none!):

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

1. You need to define a callback function that is structured like fastapi lifespans:

```python
def my_callback(input):
    print(f"BEFORE: {inputs=}")
    result = yield
    print(f"AFTER: {result=}")
```

To attach the callback function to all httpx GET calls:

```python
from common_hooks.httpx import hook
from common_hooks.conditions import HttpRequestCondition # optional condition

complex_condition = HttpRequestCondition(methods=["GET"])
hook.attach(my_callback, condition=complex_condition)
```

To attach a callback function to all httpx POST calls:

```python
from common_hooks.httpx import hook
from common_hooks.conditions import HttpRequestCondition

complex_condition = HttpRequestCondition(methods=["POST"]) # optional
hook.attach(my_callback, condition=complex_condition)
```

After attaching, you must install the hook to apply the callback(s):

```python
hook.install()
```

To use multiple hooks in the same script rename them using "as", common conditions can be reused:

```python
from common_hooks.conditions import HttpRequestCondition
from common_hooks.httpx import hook as httpx_hook
from common_hooks.fastapi import hook as fastapi_hook

complex_condition = HttpRequestCondition(methods=["POST"])

hook.attach(my_callback, condition=complex_condition)
httpx_hook.install()

fastapi_hook.attach(my_callback, condition=complex_condition)
fastapi_hook.install()
```
This script will apply the callback to all POST requests made by httpx and all POST requests received by fastapi.

## Planned future hooks (Still needs POC)

- aiohttp
- requests

## Possible future hook ideas

- flask
- django
- sqlalchemy
- inbuilt functions
- inbuilt classes

## Contribution

If you have a hook you would like to add, please create a pull request with the hook and a test to ensure it works as expected.
A hook must inherit from the CoreHook class you can import using:

```python
from common_hooks import CoreHook
```

Check implementation of other hooks to see how to implement your own.
