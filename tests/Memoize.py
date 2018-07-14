class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        key = tuple(sorted(args))
        if key not in self.memo:
            self.memo[key] = self.f(*args)
        return self.memo[key]
