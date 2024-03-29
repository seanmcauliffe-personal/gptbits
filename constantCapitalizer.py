import ast
import astunparse
import os

class ConstantToUppercase(ast.NodeTransformer):
    def __init__(self):
        self.constants = set()
        self.assigned = set()

    def visit_Assign(self, node):
        # Handle function call assignments
        if isinstance(node.value, ast.Call):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.constants.discard(target.id)
                    self.assigned.add(target.id)
        else:
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id not in self.assigned:
                    self.constants.add(target.id)
                elif isinstance(target, ast.Name):
                    self.constants.discard(target.id)
                self.assigned.add(target.id)

        return self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and isinstance(node, ast.Name) and node.id in self.constants:
            old_name = node.id
            node.id = node.id.upper()
            return (old_name, node)
        return node


def process_file(file_path):
    with open(file_path, "r") as source:
        tree = ast.parse(source.read())

    transformer = ConstantToUppercase()
    modified_tree = transformer.visit(tree)

    # Gather changed variable names and their locations
    changed_vars = []
    for old_name, node in ast.walk(tree):
        if isinstance(node, tuple):
            line_number = node[1].lineno
            changed_vars.append((old_name, line_number))

    if changed_vars:
        print(f"In file {file_path}, changed the following variables:")
        for old_name, line_number in changed_vars:
            print(f"{old_name} at line {line_number} -> {old_name.upper()}")

    new_code = astunparse.unparse(tree)

    with open(file_path, "w") as source:
        source.write(new_code)


def process_directory(dir_path):
    """
    Process all .py files in the given directory and its subdirectories
    """
    # Walk through all files in the directory
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                process_file(file_path)


if __name__ == "__main__":
    # Replace this with the path to your directory
    process_directory("/path/to/your/directory")
