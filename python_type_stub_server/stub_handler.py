class StubHandler:
    def __init__(self, modules_to_stubs: dict[str, str]):
        self.modules_to_stubs = modules_to_stubs
        self.modules = [key for key in sorted(modules_to_stubs.keys())]

    def get_modules(self) -> list[str]:
        return self.modules

    def get_modules_for_prefix(self, module_prefix) -> list[str]:
        return [module for module in self.modules if module.startswith(module_prefix)]

    def get_stub(self, module: str) -> str:
        return self.modules_to_stubs[module]
