import json
import os

from fastapi import FastAPI, HTTPException

from python_type_stub_server.function_handler import FunctionHandler
from python_type_stub_server.stub_handler import StubHandler

monkey_type_json_path = os.environ["MONKEY_TYPE_JSON"]
monkey_type_functions_json_path = os.environ["MONKEY_TYPE_FUNCTIONS_JSON"]

with open(monkey_type_json_path, "r") as monkey_type_file:
    monkey_type_modules_to_stubs = json.load(monkey_type_file)
    monkey_stub_handler = StubHandler(monkey_type_modules_to_stubs)

with open(monkey_type_functions_json_path, "r") as monkey_type_functions_file:
    monkey_type_functions_to_info = json.load(monkey_type_functions_file)
    monkey_function_handler = FunctionHandler(monkey_type_functions_to_info)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/modules")
def get_modules():
    return monkey_stub_handler.get_modules()


@app.get("/stubs/{module_path}")
def get_stub_for_module(module_path: str):
    try:
        return {"stub": monkey_stub_handler.get_stub(module_path)}
    except KeyError:
        raise HTTPException(status_code=404, detail="Module not found")


@app.get("/functions")
def get_modules():
    return monkey_function_handler.get_functions()


@app.get("/functions/{function_name}")
def get_modules(function_name: str):
    try:
        return monkey_function_handler.get_function_info(function_name)
    except KeyError:
        raise HTTPException(status_code=404, detail="Function not found")
