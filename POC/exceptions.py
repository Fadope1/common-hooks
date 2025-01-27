"""POC for capturing exceptions."""

""" 1. This only captures if the exception is raised outside the try block."""

import sys


def custom_exception_handler(exc_type, exc_value, exc_traceback):
    print(f"Exception caught: {exc_type.__name__}: {exc_value}")


# Set the custom exception handler
sys.excepthook = custom_exception_handler

# Example of an unhandled exception
raise ValueError("This is a test exception")

""" 2. This captures if the exception is raised inside the try block."""

import sys


def trace_exceptions(frame, event, arg):
    if event == "exception":
        exc_type, exc_value, exc_traceback = arg
        print(f"[sys.settrace] Exception: {exc_type.__name__}, {exc_value}")

    return trace_exceptions


sys.settrace(trace_exceptions)  # Set trace inside the function


def main():
    try:
        raise ValueError("This is a handled exception")
    except ValueError:
        pass


main()
