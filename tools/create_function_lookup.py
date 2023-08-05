import ast
import dataclasses
import json
from dataclasses import dataclass
from typing import Annotated

import typer


@dataclass
class Function:
    name: str
    stub_line: int


class StubVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.functions.append(Function(node.name, node.lineno))


def main(
        stub_path: Annotated[str, typer.Argument(help="Path to the stub json")],
        output_path: Annotated[str, typer.Argument(help="Path to write the output to")]
):
    with open(stub_path, "r") as stub_file:
        module_to_stubs_dictionary = json.load(stub_file)
        function_lookup_dict = {}
        for module in module_to_stubs_dictionary:
            stubs = module_to_stubs_dictionary[module]
            parsed_stubs = ast.parse(stubs)
            stub_visitor = StubVisitor()
            stub_visitor.visit(parsed_stubs)
            for function in stub_visitor.functions:
                function_info = function_lookup_dict.get(function.name, [])
                function_info.append({"module": module, "stub_line": function.stub_line})
                function_lookup_dict[function.name] = function_info
        with open(output_path, "w") as output_file:
            json.dump(function_lookup_dict, output_file)


if __name__ == "__main__":
    typer.run(main)
