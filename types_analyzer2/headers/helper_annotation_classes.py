from . import base_types_0
class _round_return_type(base_types_0._scriptable_match):
    def evaluate(self, kwlist_args, kwdict_args):
        if len(kwlist_args) < 2 and not "ndigits" in kwdict_args:
            return "int"
        elif "number" in kwdict_args:
            return kwdict_args["number"]
        else:
            return kwlist_args[0]

class _min_max_return_type(base_types_0._scriptable_match):
    def evaluate(self, kwlist_args, kwdict_args):
        if len(kwlist_args)==1 and isinstance(kwlist_args, list):
            alist = kwlist_args[0]
            return self.typestable.find_common_type_parent(alist)
        else:
            return self.typestable.find_common_type_parent(kwlist_args)

class _zip_return_type(base_types_0._scriptable_match):
    def evaluate(self, kwlist_args, kwdict_args):
        if kwlist_args:
            value_types = []
            for typee in kwlist_args:
                value_type = typee.valuetype
                value_types.append(value_type)
            tuple_type = self.typestable.lookup_or_create_parametrized_tuple(value_types)
            return self.typestable.lookup_or_create_parametrized_list(tuple_type, "_sequence")
        else:
            return "list"