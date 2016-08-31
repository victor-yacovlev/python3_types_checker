import ast


class CompileError(BaseException):
    def __init__(self, lineno: int, col_offset):
        super().__init__()
        self.lineno = lineno
        self.col_offset = col_offset

    def __repr__(self):
        if hasattr(self, "message"):
            return "Error: '" + self.message + "' at " + str(self.lineno)
        else:
            return "Error " + self.__class__.__name__ + " at " + str(self.lineno)


class UnsupportedOperandTypesCompileError(CompileError):
    def __init__(self, lineno, col_offset, op, left_type, right_type):
        super().__init__(lineno, col_offset)
        self.op = op
        self.left_type = left_type
        self.right_type = right_type


class NoSuchMethodCompileError(CompileError):
    def __init__(self, lineno, col_offset, instance_type, name):
        super().__init__(lineno, col_offset)
        self.instance_type = instance_type
        self.name = name


class ReturnFromWrongScopeCompileError(CompileError):
    def __init__(self, lineno, col_offset):
        super().__init__(lineno, col_offset)


class MatchError(BaseException):
    def __init__(self, method):
        self.method = method


class IncompatibleBinaryOperationCompileError(CompileError):
    def __init__(self, lineno: int, col_offset: int, left_type, right_type, op):
        super().__init__(lineno, col_offset)
        self.op = op
        self.left_type = left_type
        self.right_type = right_type


class NoEnoughtParametersMatchError(MatchError):
    def __init__(self, arg_name_not_provided: str):
        self.arg_name_not_provided = arg_name_not_provided


class ExtraArgumentsMatchError(MatchError):
    def __init__(self, method, provided_count):
        super().__init__(method)
        self.provided_count = provided_count


class NoEnoughtArgumentsMatchError(MatchError):
    def __init__(self, method, provided_count):
        super().__init__(method)
        self.provided_count = provided_count


class MethodDoesNotAllowKwdictMatchError(MatchError):
    def __init__(self, method, provided_keys):
        super().__init__(method)
        self.provided_keys = provided_keys


class TypeMismatchMatchError(MatchError):
    def __init__(self, method, argument, provided_type):
        super().__init__(method)
        self.argument = argument
        self.provided_type = provided_type

    def to_compile_error(self, node):
        m = self

        class TypeMismatchCompileError(CompileError):
            def __init__(self):
                super().__init__(node.lineno, node.col_offset)
                self.required_type = repr(m.argument)
                self.provided_type = repr(m.provided_type)
                self.message = "Type mismatch (expected " + repr(m.argument) + ", but got " + repr(
                    m.provided_type) + ")"

        return TypeMismatchCompileError()


class LambdaArgumentReturnTypeMatchError(MatchError):
    def __init__(self, method, required_return_type, lambda_return_type):
        super().__init__(method)
        self.required_return_type = required_return_type
        self.lambda_return_type = lambda_return_type

    def to_compile_error(self, node):
        m = self

        class LambdaArgumentReturnTypeCompileError(CompileError):
            def __init__(self):
                super().__init__(node.lineno, node.col_offset)
                self.required_return_type = repr(m.required_return_type)
                self.lambda_return_type = repr(m.lambda_return_type)
                self.message = "Lambda return type mismatch " + \
                               "(expected " + self.required_return_type + ", but got " + self.lambda_return_type + ")"

        return LambdaArgumentReturnTypeCompileError()


class NoEnoughtParametersCompileError(CompileError):
    def __init__(self, lineno, col_offset, arg_name_not_provided):
        super().__init__(lineno, col_offset)
        assert isinstance(arg_name_not_provided, str)
        self.arg_name_not_provided = arg_name_not_provided


class WrongTupleAssignmentCompileError(CompileError):
    def __init__(self, lineno, col_offset, lvalue_count, rvalue_count):
        super().__init__(lineno, col_offset)
        self.lvalue_count = lvalue_count
        self.rvalue_count = rvalue_count


def transform_match_error_to_compile_error(match_error: MatchError, node):
    if hasattr(match_error, "to_compile_error"):
        transform_func = match_error.to_compile_error
        return transform_func(node)
    else:
        result = CompileError(node.lineno, node.col_offset)
        if hasattr(match_error, "message"):
            result.message = match_error.message
        else:
            result.message = repr(match_error)
        return result
