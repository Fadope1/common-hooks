class TrioExcepthookHandler:
    def install(
        self,
        callback: SyncCallback,
        condition: ExceptionCondition,
    ) -> None:
        if trio is None:
            warnings.warn("Trio is not available, skipping Trio exception handler.")
            return

        async def trio_handle_exception(
            exc_type: type[BaseException],
            exc_value: BaseException,
            exc_traceback: TracebackType,
        ) -> None:
            if condition.matches(exc_type, False):
                for _ in callback(exc_type, exc_value, exc_traceback, False):
                    pass
            else:
                trio.lowlevel._run_trio_excepthook(exc_type, exc_value, exc_traceback)

        trio.hazmat.install_global_exception_handler(trio_handle_exception)
