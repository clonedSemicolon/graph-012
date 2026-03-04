import logging
import inspect
from dynapyt.analyses.BaseAnalysis import BaseAnalysis


class CallTrace(BaseAnalysis):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        handler = logging.FileHandler("output.log", "w", "utf-8")
        handler.setFormatter(logging.Formatter("%(message)s"))
        root_logger.addHandler(handler)

    def _resolve_location(self, dyn_ast, iid):
        try:
            loc = self.iid_to_location(dyn_ast, iid)
            return f"{loc.file}:{loc.start_line}:{loc.start_column}"
        except Exception:
            return f"{dyn_ast}:-1:-1"

    def _get_func_info(self, function):
        func_name = getattr(
            function,
            "__qualname__",
            getattr(function, "__name__", str(function)),
        )
        mod = inspect.getmodule(function)
        module_name = getattr(mod, "__name__", "unknown")
        return module_name, func_name

    def pre_call(self, dyn_ast, iid, function, pos_args, kw_args):
        loc = self._resolve_location(dyn_ast, iid)
        module_name, func_name = self._get_func_info(function)
        logging.info(f"CALL {loc} -> {module_name}.{func_name}")

    def post_call(self, dyn_ast, iid, result, call, pos_args, kw_args):
        loc = self._resolve_location(dyn_ast, iid)
        _, func_name = self._get_func_info(call)
        logging.info(f"RETURN {loc} <- {func_name}")

    def function_enter(self, dyn_ast, iid, args, name, is_lambda):
        loc = self._resolve_location(dyn_ast, iid)
        logging.info(f"ENTER {loc} {name}")

    def function_exit(self, dyn_ast, function_iid, name, result):
        logging.info(f"EXIT {name}")

    def end_execution(self):
        logging.info("END EXECUTION")
