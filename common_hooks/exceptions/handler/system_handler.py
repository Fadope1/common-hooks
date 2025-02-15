class SysExcepthookHandler:
    def install(
        self,
        callback: SyncCallback,
        condition: ExceptionCondition,
    ) -> None:
        sys.excepthook = partial(self.handle_exception, callback=callback, condition=condition)

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
