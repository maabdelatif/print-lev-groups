"""
    Memoize class
"""
class Memoize: #pylint: disable=too-few-public-methods
    """
        Remebers the results of a expensive function as it
        is not cheap to recompute
        The ordered arguments of the function are stored as the
        keys
    """
    def __init__(self, function):
        self.function = function
        self.memo = {}

    def __call__(self, *args):
        key = tuple(sorted(args))
        if key not in self.memo:
            self.memo[key] = self.function(*args)
        return self.memo[key]
