import inspect
import importlib

def list_functions(module):
    functions = []
    for name, obj in inspect.getmembers(module, inspect.isfunction):
        if obj.__module__ == module.__name__:
            functions.append(name)
    return functions

def test_list_functions():
    library_name = 'textilefactorylib'  # Replace with the name of your library
    library = importlib.import_module(library_name)

    # Get all submodules and subpackages
    submodules = []
    for name, obj in inspect.getmembers(library):
        if inspect.ismodule(obj) and obj.__name__.startswith(library_name):
            submodules.append(obj)

    # Print all functions in each submodule
    for submodule in submodules:
        print(f"Functions in {submodule.__name__}:")
        functions = list_functions(submodule)
        for func in functions:
            print(func)

if __name__ == '__main__':
    print(list_functions("textilefactorylib"))
    import pytest
    pytest.main()