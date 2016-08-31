## Fully annotated function declaration and usage
def annotated_func(a: int, b: float, c) -> float:  # last argument not annotated and not in use
    return a + b

annotated_func_1 = annotated_func(1, 2, 3)  # expects: float  ### annotated_func_1: float

## Return type can be constructed from arguments
def annotated_only_args(a: int, b: float):
    res = a + b
    return res

annotated_only_args_1 = annotated_only_args(1, 2)  # expects: float  ### annotated_only_args_1: float

## Arguments annotated via assert isinstance
def annotated_assert_isinstance_arguments(a, b):
    assert isinstance(a, int)
    assert isinstance(b, float)
    return a + b

annotated_assert_isinstance_arguments_1 = annotated_assert_isinstance_arguments(1, 2)  # expects: float  ### annotated_assert_isinstance_arguments_1: float

## Function that returns somthing of detectable type
def function_returns():
    return "abc"

function_returns_1 = function_returns()  # expects: str  ### function_returns_1: str