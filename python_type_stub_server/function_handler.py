class FunctionHandler:
    def __init__(self, functions_to_info: dict[str, str]):
        self.functions_to_info = functions_to_info
        self.functions = [key for key in sorted(functions_to_info.keys())]

    def get_functions(self) -> list[str]:
        return self.functions

    def get_function_info(self, function) -> dict[str, dict[str, str]]:
        return self.functions_to_info[function]
