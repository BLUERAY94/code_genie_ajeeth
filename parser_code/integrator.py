import os
import pickle
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()  # Load variables from .env file
os.environ['OPENAI_API_KEY'] = ""
# Initialize OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

class FunctionNode:
    def __init__(self, name, params, file, line):
        self.name = name
        self.params = params
        self.file = file
        self.line = line
        self.called_functions = []

    def __repr__(self):
        return f"FunctionNode(name={self.name}, params={self.params}, file={self.file}, line={self.line}, called_functions={self.called_functions})"

# Load the function tree from the file
with open('D:/c_ai_browser/function_tree.pkl', 'rb') as f:
    function_tree = pickle.load(f)

def query_function_tree(query, function_tree):
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": query},
        ],
        model="gpt-3.5-turbo",
    )
    generated_text = response.choices[0].message['content'].strip()
    
    # Extract function name from the generated text (simple heuristic)
    function_name = generated_text.split()[-1]
    
    if function_name in function_tree:
        return function_tree[function_name]
    else:
        return "Function not found."

def main():
    while True:
        query = input("Enter your query: ")
        if query.lower() == 'exit':
            break
        result = query_function_tree(query, function_tree)
        print(result)

if __name__ == "__main__":
    main()
