#!/usr/bin/env python3

import inspect

def extra_funcs(*funcs):
    """Decorator which adds extra functions to be downloaded to the pyboard."""
    def extra_funcs_decorator(real_func):
        def wrapper(*args, **kwargs):
          return real_func(*args, **kwargs)
        wrapper.extra_funcs = [*funcs]
        wrapper.source = inspect.getsource(real_func)
        wrapper.name = real_func.__name__
        return wrapper
    return extra_funcs_decorator

def foo1():
    print('foo1')

def foo2():
    print('foo2')

@extra_funcs(foo1, foo2)
def bar():
    print('bar')

def test_func(func):
    if hasattr(func, 'extra_funcs'):
        print('test_func: extra_funcs =', func.extra_funcs)
    else:
        print('test_func: no extra_funcs')

test_func(bar)
