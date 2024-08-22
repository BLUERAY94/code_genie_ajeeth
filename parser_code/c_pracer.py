
import pickle
from pycparser import c_parser, c_ast
from tree_format import create_tree_png
import os

class FunctionNode:
    def __init__(self, name, params, file, line):
        self.name = name
        self.params = params
        self.file = file
        self.line = line
        self.called_functions = []
        self.local_variables = []

    def __repr__(self):
        return (f"FunctionNode(name={self.name}, params={self.params}, file={self.file}, "
                f"line={self.line}, called_functions={self.called_functions}, "
                f"local_variables={self.local_variables})")

class GlobalVariableNode:
    def __init__(self, name, type, file, line):
        self.name = name
        self.type = type
        self.file = file
        self.line = line

    def __repr__(self):
        return f"GlobalVariableNode(name={self.name}, type={self.type}, file={self.file}, line={self.line})"

class FunctionVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.functions = {}
        self.current_function = None

    def visit_FuncDef(self, node):
        func_name = node.decl.name
        if node.decl.type.args:
            params = [param.name for param in node.decl.type.args.params if param.name]
        else:
            params = [] 
        file = node.coord.file
        line = node.coord.line
        func_node = FunctionNode(func_name, params, file, line)
        self.functions[func_name] = func_node
        self.current_function = func_name
        self.generic_visit(node)  # Continue visiting children
        self.current_function = None

    def visit_Decl(self, node):
        if isinstance(node.type, c_ast.TypeDecl):
            var_name = node.name
            if self.current_function:  # Local variable
                self.functions[self.current_function].local_variables.append(var_name)
        self.generic_visit(node)  # Continue visiting children

    def visit_FuncCall(self, node):
        if isinstance(node.name, c_ast.ID):
            caller_name = self.current_function
            if caller_name:
                caller_node = self.functions.get(caller_name)
                if caller_node:
                    caller_node.called_functions.append(node.name.name)
        self.generic_visit(node)

class GlobalVariableVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.global_variables = {}

    def visit_Decl(self, node):
        if isinstance(node.type, c_ast.TypeDecl):
            var_name = node.name
            var_type = node.type.type.names if isinstance(node.type.type, c_ast.IdentifierType) else None
            file = node.coord.file
            line = node.coord.line
            if not hasattr(node, 'funcspec'):  # Ensure it's not a function declaration
                global_var = GlobalVariableNode(var_name, var_type, file, line)
                self.global_variables[var_name] = global_var
        self.generic_visit(node)  # Continue visiting children

def clean_preprocessed_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = [line for line in lines if not '#include "vadefs.h"' in line]

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)

def parse_c_codebase(file_path):
    function_index = {}
    global_variable_index = {}
    parser = c_parser.CParser()

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            code = f.read()
            ast = parser.parse(code, filename=file_path)
            function_visitor = FunctionVisitor()
            function_visitor.visit(ast)
            function_index.update(function_visitor.functions)
            
            global_variable_visitor = GlobalVariableVisitor()
            global_variable_visitor.visit(ast)
            global_variable_index.update(global_variable_visitor.global_variables)
        except Exception as e:
            print(f"Skipping {file_path} due to error: {e}")
    return function_index, global_variable_index

def load_pickle_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            return data
    except Exception as e:
        print(f"An error occurred while loading the pickle file: {e}")
        return None

def inspect_data(data):
    if data is None:
        print("No data to inspect.")
        return

    if isinstance(data, (dict, list, set)):
        print(data)
    else:
        print(f"Data type: {type(data)}")
        print(data)

def main():
    codebase_path = "D:\Code_genie\Kishore\parser_code\memmgr.i"
    #codebase_path = "D:/code/project_1/output_file/preprocessed.i"
    
    if os.path.isfile('function_tree2.pkl') and os.path.isfile('global_variables2.pkl'):
        pass
    else:
        function_tree, global_variables = parse_c_codebase(codebase_path)
    
        with open('function_tree2.pkl', 'wb') as f:
            pickle.dump(function_tree, f)
        with open('global_variables2.pkl', 'wb') as f:
            pickle.dump(global_variables, f)

    function_data = load_pickle_file('function_tree2.pkl')
    global_data = load_pickle_file('global_variables2.pkl')

    print("Functions:")
    inspect_data(function_data)
    
    print("\nGlobal Variables:")
    inspect_data(global_data)

    print('Done')

    create_tree_png('function_tree2')
    create_tree_png('global_variables2')


if __name__ == "__main__":
    main()
