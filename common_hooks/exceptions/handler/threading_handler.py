class ThreadingExcepthookHandler:
    def install(
        self,
        callback: SyncCallback,
        condition: ExceptionCondition,
    ) -> None:
        def handle_threading_excepthook(args: threading.ExceptHookArgs) -> None:
            self.handle_exception(
                args.exc_type,
                args.exc_value,
                args.exc_traceback,
                callback=callback,
                condition=condition,
            )

        threading.excepthook = handle_threading_excepthook

    def handle_exception(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType,
        *,
        callback: SyncCallback,
        condition: ExceptionCondition,
    ) -> None:
        if condition.matches(exc_type, False):
            for _ in callback(exc_type, exc_value, exc_traceback, False):
                pass
        else:
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
