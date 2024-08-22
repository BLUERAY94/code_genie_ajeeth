import pickle
import csv

class FunctionNode:
    def __init__(self, name, params, file, line):
        self.name = name
        self.params = params
        self.file = file
        self.line = line
        self.called_functions = []
    def __repr__(self):
        return f"FunctionNode(name={self.name}, params={self.params}, file={self.file}, line={self.line}, called_functions={self.called_functions})"

# Function to traverse the tree and collect data
def traverse_and_collect(node, depth=0, parent_name=None):
    rows = []

    if isinstance(node, FunctionNode):
        # Create a CSV row
        row = {
            'Function Name': node.name,
            'Parent Function': parent_name,
            'Call Depth': depth,
            'Parameters': node.params,
            'File': node.file,
            'Line Number': node.line
        }
        rows.append(row)
        
        # Traverse called functions
        for child in node.called_functions:
            rows.extend(traverse_and_collect(child, depth + 1, node.name))
    elif isinstance(node, str):
        # If the node is a string, just create a row with the function name
        row = {
            'Function Name': node,
            'Parent Function': parent_name,
            'Call Depth': depth,
            'Parameters': None,
            'File': None,
            'Line Number': None
        }
        rows.append(row)

    return rows

# Load the tree from the .pkl file
with open('D:/c_ai_browser/function_tree.pkl', 'rb') as file:
    data = pickle.load(file)

rows = []

# Check if the loaded data is a dictionary
if isinstance(data, dict):
    for key, root_node in data.items():
        rows.extend(traverse_and_collect(root_node))
else:
    rows = traverse_and_collect(data)

# Write the data to a CSV file
csv_file = 'D:/output_file/function_calls.csv'
with open(csv_file, 'w', newline='') as csvfile:
    fieldnames = ['Function Name', 'Parent Function', 'Call Depth', 'Parameters', 'File', 'Line Number']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(rows)

print(f"Function call tree saved to {csv_file}")
