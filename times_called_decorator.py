def limit_call_times(limit):
    def decorator(func):
        def wrapper(*args, **kwargs):
            wrapper.counter += 1
            if wrapper.counter > limit:
                raise Exception(f'call limit reached: {func.__name__}() was called {limit} times already')
            return func(*args, **kwargs)
        wrapper.counter = 0
        return wrapper
    return decorator

@limit_call_times(5)
def foo():
    print('foo')

@limit_call_times(6)
def bar():
    print('bar')

while (True):
    bar()
    foo()
    
