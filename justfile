# prints the list of available commands
default:
    just --list

# format the code via black and isort
format:
    poetry run black .; poetry run isort .

# run monkeytype on the examples directory
examples-monkeytype:
    cd examples; poetry run monkeytype run main.py

# generate stubs from the monkeytype output in the example directory
examples-stubs: examples-monkeytype
    cd examples; poetry run python ../tools/monkey_type_to_stubs.py

# generate function lookup information for the monkeytype stubs
examples-functions: examples-stubs
    cd examples; poetry run python ../tools/create_function_lookup.py MonkeyTypes.json MonkeyTypeFunctions.json

# run the test server with the example stubs
examples-api: examples-functions
    MONKEY_TYPE_JSON="examples/MonkeyTypes.json" MONKEY_TYPE_FUNCTIONS_JSON="examples/MonkeyTypeFunctions.json" poetry run uvicorn tools.test_api:app