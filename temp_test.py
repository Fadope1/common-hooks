from common_hooks.exceptions import hook
from common_hooks.conditions import ExceptionCondition

condition = ExceptionCondition(exceptions={ValueError}, check_subclass=True)


def test(*args, **kwargs):
    print("callback called", args, kwargs)
    yield
    print("callback 2")


hook.attach(test, condition=condition)
hook.install()

import threading


def raise_exception():
    print(f"test1 from thread {threading.get_ident()}")
    raise ValueError("test2")


# def main():
#     threads = []
#     for _ in range(2):
#         thread = threading.Thread(target=raise_exception)
#         threads.append(thread)
#         thread.start()

#     for thread in threads:
#         thread.join()

#     print("done")


# main()

raise ValueError("test")
