# experiment with methods of passing configurable-in-data paremeter names to functions in Python


def dummy_function(arg1: int, arg2: int = 0, arg3: bool = False):
    print("%d, %d, %s" % (arg1, arg2, arg3))


dummy_function(5, 55, True)

dummy_function(5, arg3=False)


# call dummy_function with argument names and values defined in a dictionary
#  only pass arguments that are in the dictionary. Example inputs:
# kwargs = {'arg1': 7, 'arg2': 77, 'arg3': True}
# kwargs = {'arg1': 7, 'arg2': 77}
# kwargs = {'arg3': True}
def call_with_named_args(func, kwargs):
    # get the function's signature
    import inspect

    sig = inspect.signature(func)
    # create a dictionary of the arguments to pass
    args = {}
    for name, param in sig.parameters.items():
        if name in kwargs:
            args[name] = kwargs[name]
        elif param.default is not param.empty:
            args[name] = param.default
        else:
            raise TypeError(f"{name} is a required argument")
    return func(**args)


kwargs = {"arg1": 6, "arg2": 66, "arg3": True}
call_with_named_args(dummy_function, kwargs)
kwargs = {"arg1": 6, "arg3": False}
call_with_named_args(dummy_function, kwargs)


# call dummy_function with one directly-passed argument,
#   plus an optional dictionary of additional arguments
def call_with_named_extra_args(func, arg1, kwargs={}):
    # get the function's signature
    import inspect

    sig = inspect.signature(func)
    # create a dictionary of the arguments to pass
    args = {}
    kwargs["arg1"] = arg1
    for name, param in sig.parameters.items():
        if name in kwargs:
            args[name] = kwargs[name]
        elif param.default is not param.empty:
            args[name] = param.default
        else:
            raise TypeError(f"{name} is a required argument")
    return func(**args)


call_with_named_extra_args(dummy_function, 7)
call_with_named_extra_args(dummy_function, 7, {"arg2": 77})
call_with_named_extra_args(dummy_function, 7, {"arg3": True})
