from .base_types_0 import _any
from .base_types_0 import _nth_arg_type
from .base_types_0 import _iterable
from .helper_annotation_classes import _min_max_return_type, _zip_return_type
def max(arg1: _any, arg2: _any, *args: [_any]) -> _min_max_return_type: pass
def min(arg1: _any, arg2: _any, *args: [_any]) -> _min_max_return_type: pass
def zip(*iterables: [_iterable]) -> _zip_return_type: pass