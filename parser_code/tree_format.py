import os
import pickle
from graphviz import Digraph
from IPython.display import Image, display
# Specify the path to the Graphviz executable
#os.environ["PATH"] += os.pathsep + 'C:\\graph\\windows_10_cmake_Release_Graphviz-12.0.0-win64 (1)\\Graphviz-12.0.0-win64\\bin'
os.environ["PATH"] += os.pathsep + 'D:\\Code_genie\\Kishore\\windows_10_cmake_Release_Graphviz-12.1.0-win64\\Graphviz-12.1.0-win64\\bin'


#https://graphviz.org/download/
# Define the FunctionNode class based on the provided definition
class FunctionNode:
    def __init__(self, name, params, file, line):
        self.name = name
        self.params = params
        self.file = file
        self.line = line
        self.called_functions = []

    def __repr__(self):
        return f"FunctionNode(name={self.name}, params={self.params}, file={self.file}, line={self.line}, called_functions={self.called_functions})"



def create_tree_png(pickle_name):
    # Function to add nodes and edges recursively
    def add_nodes_edges(dot, node, visited):
        if node.name in visited:
            return
        visited.add(node.name)
        
        dot.node(node.name, f"{node.name}({', '.join(node.params)})\n{node.file}:{node.line}")
        
        for called_function in node.called_functions:
            dot.edge(node.name, called_function)
            add_nodes_edges(dot, data[called_function], visited)

    
    # Now reload the pickle file with the correct class definition
    with open(("{}.pkl").format(pickle_name), 'rb') as file:
        data = pickle.load(file)

    # Display the type and structure of the loaded data
    data_type = type(data)
    print(data_type)
    data_summary = str(data)[:500]  # Limit to 500 characters for brevity

    data_type, data_summary

    # Create a directed graph
    dot = Digraph(comment='Function Call Graph')

    # Add nodes and edges to the graph
    visited = set()
    for func_name, node in data.items():
        add_nodes_edges(dot, node, visited)

    # Save and render the graph to a directory with known write permissions
    #output_directory = os.path.expanduser('~/Documents')
    output_directory    = 'D:/Code_genie/Kishore/parser_code'
    graph_path = os.path.join(output_directory, pickle_name)

    dot.render(graph_path, format='png', cleanup=True)
    print(f"Graph saved to {graph_path}.png")
