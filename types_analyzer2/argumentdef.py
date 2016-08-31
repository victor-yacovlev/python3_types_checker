import copy
import inspect


class ArgumentDef:
    def __init__(self, signature, typedef):
        assert isinstance(signature, inspect.Parameter)
        self.signature = signature
        self.typedef = typedef
        self.resolved = False

    def copy(self):
        signature = copy.copy(self.signature)
        if self.typedef is not None:
            typedef = self.typedef.copy()
        else:
            typedef = None
        return ArgumentDef(signature, typedef)

    def __repr__(self):
        r = self.signature.name
        if self.typedef:
            r += ": " + repr(self.typedef)
        if self.signature.default!=inspect.Signature.empty:
            r += " = " + repr(self.signature.default)
        return r
