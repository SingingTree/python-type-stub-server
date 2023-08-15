import json
import os
import sys
from typing import Annotated, Optional

import typer
from monkeytype import Config
from monkeytype.cli import get_monkeytype_config
from monkeytype.exceptions import MonkeyTypeError
from monkeytype.stubs import (
    ExistingAnnotationStrategy,
    Stub,
    build_module_stubs_from_traces,
)


def get_modules_to_stubs_dict(config: Config) -> Optional[dict[str, Stub]]:
    # Since monkeytype needs to import the user's code (and possibly config
    # code), the user's code must be on the Python path. But when running the
    # CLI script, it won't be. So we add the current working directory to the
    # Python path ourselves.
    sys.path.insert(0, os.getcwd())

    modules = config.trace_store().list_modules()
    modules_to_stubs = {}
    for module in modules:
        thunks = config.trace_store().filter(module)
        traces = []
        for thunk in thunks:
            try:
                traces.append(thunk.to_trace())
            except MonkeyTypeError as mte:
                print(f"WARNING: Failed decoding trace: {mte}", file=sys.stderr)
        if not traces:
            return None
        rewriter = config.type_rewriter()
        # TODO, add this back in if needed
        # if args.disable_type_rewriting:
        #     rewriter = NoOpRewriter()
        stubs = build_module_stubs_from_traces(
            traces,
            config.max_typed_dict_size(),
            existing_annotation_strategy=ExistingAnnotationStrategy.REPLICATE,
            rewriter=rewriter,
        )
        modules_to_stubs[module] = stubs.get(module, None)
    return modules_to_stubs


def main(
    monkey_type_config_path: Annotated[
        str, typer.Option(help="Path to MonkeyType config", show_default=False)
    ] = "monkeytype.config:get_default_config()",  # This is the default used by the MonkeyType CLI, so mimic that.
    output_path: Annotated[
        str, typer.Option(help="Path to write the output to")
    ] = "MonkeyTypes.json",
):
    config = get_monkeytype_config(monkey_type_config_path)
    modules_to_stubs = get_modules_to_stubs_dict(config)
    modules_to_rendered_stubs = {}
    for k in modules_to_stubs:
        print(f"{k}: {modules_to_stubs[k].render()}")
        modules_to_rendered_stubs[k] = modules_to_stubs[k].render()
    with open(output_path, "w") as type_file:
        json.dump(modules_to_rendered_stubs, type_file)


if __name__ == "__main__":
    typer.run(main)
