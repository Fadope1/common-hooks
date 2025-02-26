# Common-hooks

This package is made to provide a simple way to create hooks (callbacks) to common packages and functions/ inbuilts.
Generally speaking, its relatively simple to create a hook, you import and attach to a package.

## Next steps

[x] Create basic tests
[x] Upload to pypi
[ ] Advanced test support
[ ] Exceptions hook
[ ] Integrate requests library
[ ] Integrate aiohttp library

## Installation

There are multiple possible installations, depending on your need.

1. Simple install only the core hooks that do not require any dependencies (inbuilt hooks!):

    ```bash
    pip install common_hooks
    ```

2. Installing all (Not recommended):

    ```bash
    pip install common_hooks[all]
    ```

3. Installing only the hooks that require a specific package:

    ```bash
    pip install common_hooks[package_name]
    e.g.
    pip install common_hooks[httpx]
    ```

4. You can install multiple hooks using comma separated list, for example:

    ```bash
    pip install common_hooks[package_name,package_name2]
    e.g.
    pip install common_hooks[httpx,fastapi]
    ```

## Available hooks include

- httpx
- fastapi

## Usage

1. You need to define a callback function (similar to fastapi lifespans):

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

condition = HttpRequestCondition(methods=["GET"])
hook.attach(my_callback, condition=condition)
```

(or) To attach a callback function to all httpx POST calls:

```python
from common_hooks.httpx import hook
from common_hooks.conditions import HttpRequestCondition

condition = HttpRequestCondition(methods=["POST"]) # optional
hook.attach(my_callback, condition=condition)
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

## Planned future hooks

- exceptions
- aiohttp
- requests

## Possible future hook ideas

- flask
- django
- sqlalchemy
- inbuilt functions
- inbuilt classes

## Other ideas

- Callback decorator
- Context manager

## Contribution

If you have a hook you would like to add, please create a pull request with the hook and a test to ensure it works as expected.
A hook must inherit from the CoreHook class you can import using:

```python
from common_hooks import CoreHook
```

Check implementation of other hooks to see how to implement your own.
