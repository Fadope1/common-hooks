from common_hooks import exceptions
from common_hooks.conditions import ExceptionCondition

condition = ExceptionCondition(exceptions={ValueError})


def test(*args, **kwargs):
    print("callback called")
    yield
    print("callback 2")


exceptions.hook.attach(test, condition=condition)
exceptions.hook.install()

raise ValueError("test")
