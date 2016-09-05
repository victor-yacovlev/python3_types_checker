import symtable
import ast

from types_analyzer2.special_pseudo_types import AnyOf
from .typedefs import *
from . import typetable
from . import functable
from .type_analizer_errors import *
from .funcdefs import *
from . import parsers


class TemporarySymbolTable:
    def __init__(self, parent):
        self.parent_table = parent
        self.values = {}
        self.return_type = None

    def lookup(self, name):
        if name in self.values:
            return self.values[name]
        else:
            return self.parent_table.lookup(name)


class Visitor(ast.NodeVisitor):
    def __init__(self, symtable: symtable.SymbolTable, typetable: typetable.TypesTable,
                 functable: functable.MethodsTable):
        super().__init__()
        self.symtable = [symtable]
        self.typetable = typetable
        self.functable = functable
        self.function_scopes = []
        self.errors = []
        self.temporary_symtables = []

    def visit_Assign(self, node):
        try:
            rvalue_type = self.resolve_expression_type(node.value)
            for target in node.targets:
                self.assign_type_to_target(target, rvalue_type)
        except CompileError as error:
            self.errors.append(error)

    def visit_For(self, node):
        try:
            iterable_type = self.resolve_expression_type(node.iter)
            assert isinstance(iterable_type, TypeDef)
            iterable_value_type = iterable_type.valuetype
            if iterable_value_type is not None:
                self.assign_type_to_target(node.target, iterable_value_type)
        except CompileError as error:
            self.errors.append(error)
        super().generic_visit(node)

    def visit_Return(self, node):
        try:
            rtype = self.resolve_expression_type(node.value)
            if isinstance(self.current_symbol_table(), TemporarySymbolTable):
                self.current_symbol_table().return_type = rtype
            else:
                method = self.current_function_scope()
                if not method:
                    raise ReturnFromWrongScopeCompileError(node.lineno, node.col_offset)
                assert isinstance(method, MethodDef)
                if not method.return_type or isinstance(method.return_type, AnyType):
                    method.return_type = rtype
                elif isinstance(method.return_type, AnyOf):
                    method.return_type.variants.append(rtype)
                else:
                    anyof = AnyOf([method.return_type, rtype])
                    method.return_type = anyof
        except CompileError as error:
            self.errors.append(error)

    def resolve_assert_statements(self, node):
        ## Currently recognize only 'or' operations
        result = []
        if isinstance(node, ast.BoolOp):
            op = node.op
            if isinstance(op, ast.Or):
                for x in node.values:
                    result += self.resolve_assert_statements(x)
        elif isinstance(node, ast.Call) and node.func.id == "isinstance":
            result.append(node)
        return result

    def visit_Assert(self, node):
        statements = self.resolve_assert_statements(node.test)
        known_variables = {}
        for statement in statements:
            first_arg = statement.args[0]
            second_arg = statement.args[1]
            var_name = first_arg.id
            type_name = second_arg.id
            typee = self.typetable.lookup_by_name(type_name)
            if var_name in known_variables:
                old_type = known_variables[var_name]
                if isinstance(old_type, AnyOf):
                    old_type.variants.append(typee)
                else:
                    known_variables[var_name] = AnyOf([old_type, typee])
            else:
                known_variables[var_name] = typee
        for name, value in known_variables.items():
            symbol = self.current_symbol_table().lookup(name)
            symbol.lineno = node.lineno
            symbol.col_offset = node.col_offset
            symbol.typedef = value

    def visit_FunctionDef(self, node):
        self.push_symbol_table(node.name)
        method = parsers.parse_ast_function_def(node, self.functable, self.typetable, self.current_symbol_table())
        method.ast_visitor = self
        method.ast_node = node.body
        self.functable.append("", method)
        self.begin_function_scope(method)
        ast.NodeVisitor.generic_visit(self, node)
        self.pop_symbol_table()
        self.end_function_scope()

    def begin_function_match(self, arguments: dict):
        args_table = TemporarySymbolTable(self.current_symbol_table())
        for arg_def, arg_type in arguments.items():
            args_table.values[arg_def.signature.name] = arg_type
        self.temporary_symtables.append(args_table)

    def visit_function_body(self, nodes: list):
        for node in nodes:
            self.visit(node)

    def end_function_match(self):
        table = self.temporary_symtables.pop()
        return getattr(table, "return_type", None)

    def visit_function_lambda(self, arguments: dict, node):
        self.begin_function_match(arguments)
        rtype = self.resolve_expression_type(node)
        self.end_function_match()
        return rtype

    def resolve_expression_type(self, node):
        if isinstance(node, ast.Tuple):
            item_types = [self.resolve_expression_type(x) for x in node.elts]
            return self.typetable.lookup_or_create_parametrized_tuple(item_types)

        elif isinstance(node, ast.List):
            item_types = [self.resolve_expression_type(x) for x in node.elts]
            if len(item_types) == 0:
                result = self.typetable.lookup_by_name("list")
            else:
                common_parent = self.typetable.find_common_type_parent(item_types)
                assert isinstance(common_parent, TypeDef)
                if common_parent.name != "object":
                    result = self.typetable.lookup_or_create_parametrized_list(common_parent, "list")
                else:
                    result = self.typetable.lookup_by_name("list")
            return result

        elif isinstance(node, ast.Dict):
            item_key_types = [self.resolve_expression_type(x) for x in node.keys]
            item_val_types = [self.resolve_expression_type(x) for x in node.values]
            assert len(item_key_types) == len(item_val_types)
            if len(item_key_types) == 0:
                result = self.typetable.lookup_by_name("dict")
            else:
                common_key_parent = self.typetable.find_common_type_parent(item_key_types)
                common_val_parent = self.typetable.find_common_type_parent(item_val_types)
                result = self.typetable.lookup_or_create_parametrized_dict(common_key_parent, common_val_parent)
            return result

        elif isinstance(node, ast.Num):
            type_name = type(node.n).__name__
            return self.typetable.lookup_by_name(type_name)

        elif isinstance(node, ast.Str):
            return self.typetable.lookup_by_name("str")

        elif isinstance(node, ast.Bytes):
            return self.typetable.lookup_by_name("bytes")

        elif isinstance(node, ast.UnaryOp):
            operand_type = self.resolve_expression_type(node.operand)
            if operand_type is None:
                return None

            assert isinstance(operand_type, typetable.TypeDef)
            if isinstance(node.op, ast.USub):
                op_name = "__neg__"
            else:
                op_name = "__pos__"
            methods = list(self.find_all_instance_methods(operand_type, op_name))
            if not methods:
                raise UnsupportedOperandTypesCompileError(node.lineno, node.col_offset, node.op, None, operand_type)

            match_error = None
            ## Try to match found methods and select first matching one
            for method in methods:
                assert isinstance(method, MethodDef)
                kwdict = {}
                try:
                    return_type = self.functable.match(method, [operand_type], self.typetable, kwdict, operand_type)
                except MatchError as e:
                    return_type = None
                    if not match_error: match_error = e  ## display first match error
                if return_type is not None:
                    match_error = None
                    break
            if match_error:
                raise transform_match_error_to_compile_error(match_error)
            return return_type

        elif isinstance(node, ast.Compare):
            current_type = self.resolve_expression_type(node.left)
            assert isinstance(current_type, typetable.TypeDef)
            for op, next_operand in zip(node.ops, node.comparators):
                op_name = type(op).__name__
                op_py_name = "__" + op_name.lower() + "__"
                operand_type = self.resolve_expression_type(next_operand)
                assert isinstance(operand_type, typetable.TypeDef)
                methods = list(self.find_all_instance_methods(current_type, op_py_name))
                if not methods:
                    raise UnsupportedOperandTypesCompileError(node.lineno, node.col_offset,
                                                              op, current_type,
                                                              operand_type)
                match_error = None
                ## Try to match found methods and select first matching one
                for method in methods:
                    assert isinstance(method, MethodDef)
                    args = [current_type, operand_type]
                    kwdict = {}
                    try:
                        return_type = self.functable.match(method, args, self.typetable, kwdict, current_type)
                    except MatchError as e:
                        return_type = None
                        if not match_error: match_error = e  ## display first match error
                    if return_type is not None:
                        match_error = None
                        break
                if match_error:
                    raise transform_match_error_to_compile_error(match_error, node)
                current_type = operand_type
            return return_type  ## is it always "bool" ?

        elif isinstance(node, ast.BinOp):
            left_argument_type = self.resolve_expression_type(node.left)
            right_argument_type = self.resolve_expression_type(node.right)
            if left_argument_type is None or right_argument_type is None:
                return None  # in case of non-annotated item in expression

            ## If there was an error while resolving subexpressions,
            ## it should be raised before, so all types are known
            assert isinstance(left_argument_type, typetable.TypeDef)
            assert isinstance(right_argument_type, typetable.TypeDef)

            op_name = type(node.op).__name__
            op_py_name = "__" + op_name.lower()[:3] + "__"
            alt_op_py_name = "__r" + op_name.lower()[:3] + "__"
            methods = list(self.find_all_instance_methods(left_argument_type, op_py_name)) + \
                      list(self.find_all_instance_methods(right_argument_type, alt_op_py_name))
            if not methods:
                raise UnsupportedOperandTypesCompileError(node.lineno, node.col_offset, node.op, left_argument_type,
                                                          right_argument_type)

            match_error = None
            ## Try to match found methods and select first matching one
            for method in methods:
                assert isinstance(method, MethodDef)
                if method.name == op_py_name:
                    instance_object = left_argument_type
                    args = [left_argument_type, right_argument_type]
                else:
                    instance_object = right_argument_type
                    args = [right_argument_type, left_argument_type]
                kwdict = {}
                try:
                    return_type = self.functable.match(method, args, self.typetable, kwdict, instance_object)
                except MatchError as e:
                    return_type = None
                    if not match_error: match_error = e  ## display first match error
                if return_type is not None:
                    match_error = None
                    break
            if match_error:
                raise transform_match_error_to_compile_error(match_error, node)
            return return_type

        elif isinstance(node, ast.Name):
            st = self.current_symbol_table()
            symbol = st.lookup(node.id)
            if isinstance(symbol, TypeDef):
                return symbol
            if hasattr(symbol, "typedef"):
                symbol_type = symbol.typedef
                return symbol_type
            ## Check if symbol is function
            methods = self.functable.lookup_functions_by_name(node.id)
            if methods:
                assert isinstance(methods[0], MethodDef)
                return methods[0].to_callable_type()

        elif isinstance(node, ast.NameConstant):
            value = node.value
            type_name = type(value).__qualname__
            value_type = self.typetable.lookup_by_name(type_name)
            return value_type

        elif isinstance(node, ast.Call):
            assert isinstance(node.func, ast.Attribute) or isinstance(node.func, ast.Name)
            args = []
            kwdict = {}
            for arg in node.args:
                arg_type = self.resolve_expression_type(arg)
                args.append(arg_type)
            if isinstance(node.func, ast.Attribute):
                instance_type = self.resolve_expression_type(node.func.value)
                if not instance_type:
                    return None
                assert isinstance(instance_type, TypeDef)
                args = [instance_type] + args  ## prepend 'self' parameter to args list
                method_name = node.func.attr
                methods = self.find_all_instance_methods(instance_type, method_name)
            else:
                instance_type = None
                method_name = node.func.id
                methods = self.functable.lookup_functions_by_name(method_name)
            if not methods:
                raise NoSuchMethodCompileError(node.lineno, node.col_offset, instance_type, method_name)
            ## Try to match found methods and select first matching one
            match_error = None
            for method in methods:
                assert isinstance(method, MethodDef)
                try:
                    return_type = self.functable.match(method, args, self.typetable, kwdict, instance_type)
                except MatchError as e:
                    return_type = None
                    if not match_error: match_error = e  ## display first match error
                if return_type is not None:
                    match_error = None
                    break
            if match_error:
                compile_error = transform_match_error_to_compile_error(match_error, node)
                assert isinstance(compile_error, CompileError)
                raise compile_error
            return return_type

        elif isinstance(node, ast.Lambda):
            arg_names = []
            for arg in node.args.args:
                assert isinstance(arg, ast.arg)
                arg_name = arg.arg
                arg_names.append(arg_name)
            lambda_type = Lambda(arg_names, node.body)
            lambda_type.ast_visitor = self
            # lambda_type = TypedCallable(self.typetable.lookup_by_name("object"), [AnyType() for _ in node.args.args])
            ## TODO specialuze lambda typed callable from lambda body
            return lambda_type

    def assign_type_to_target(self, target, rvalue_type):
        assert isinstance(rvalue_type, TypeDef)
        if isinstance(target, ast.Tuple):
            if len(rvalue_type.tupleitems) != len(target.elts):
                raise WrongTupleAssignmentCompileError(target.lineno, target.col_offset, len(target.elts),
                                                       len(rvalue_type.tupleitems))
            for child, rvalue_entry in zip(target.elts, rvalue_type.tupleitems):
                self.assign_type_to_target(child, rvalue_entry)
        elif isinstance(target, ast.Name):
            st = self.current_symbol_table()
            symbol = st.lookup(target.id)
            symbol.typedef = rvalue_type
            symbol.lineno = target.lineno
            symbol.col_offset = target.col_offset

    def find_all_instance_methods(self, clazz: TypeDef, name: str):
        result = self.functable.lookup_methods_by_fully_qualified_name(clazz.name, name)
        for super in clazz.supertypes:
            result += self.functable.lookup_methods_by_fully_qualified_name(super.name, name)
        return result

    def current_symbol_table(self):
        if self.temporary_symtables:
            return self.temporary_symtables[-1]
        else:
            return self.symtable[-1]

    def push_symbol_table(self, children_name: str):
        current_table = self.symtable[-1]
        assert isinstance(current_table, symtable.SymbolTable)
        child_tables = current_table.get_children()
        for table in child_tables:
            table_name = table.get_name()
            if table_name == children_name:
                self.symtable.append(table)
                return
        raise AttributeError("Table not found for children name: " + children_name)

    def pop_symbol_table(self):
        self.symtable.pop()

    def begin_function_scope(self, method: MethodDef):
        self.functable.append("", method)
        self.function_scopes.append(method)

    def end_function_scope(self):
        self.function_scopes.pop()

    def current_function_scope(self):
        if self.function_scopes:
            return self.function_scopes[-1]
        else:
            return None
