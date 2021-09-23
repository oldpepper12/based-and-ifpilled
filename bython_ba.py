import ast
from typing import List, Union
import webbrowser
import sys
from dataclasses import dataclass
import re
from termcolor import colored
import os


@dataclass
class Issue:
    message: str
    at_node: Union[ast.AST, ast.stmt]


class BythonBTW:
    def __init__(self, src: str):
        self.src = src
        self.root_node = ast.parse(self.src)
        self._issues: List[Issue] = []

    def run_evaluation(self):
        self._visit_node(self.root_node)

    def create_issue(self, message: str, at_node: Union[ast.AST, ast.stmt]):
        self._issues.append(Issue(message=message, at_node=at_node))
        # Sort issues by line
        self._issues.sort(key=lambda x: x.at_node.lineno)

    def on_visit_node(self, node: ast.AST):
        if isinstance(node, ast.FunctionDef):
            body = node.body
            does_docstring_exist = False

            if len(body):
                first_stmt = body[0]
                if isinstance(first_stmt, ast.Expr):
                    val = first_stmt.value

                    if isinstance(val, ast.Constant):
                        if isinstance(val.value, str):
                            self.on_visit_docstring(val.value, val)
                            does_docstring_exist = True
            
            if not does_docstring_exist:
                self.create_issue(
                    "No docstring found???? how tf are ppl supposed to know how to use ur function?",
                    node
                )

        if isinstance(node, ast.If):
            self.create_issue(
                "If statement detected. Extremely based and geniepilled", node)

    def on_visit_docstring(self, docstring: str, docstring_node: ast.Constant):
        docstring = docstring.strip()
        if len(docstring) < 50:
            self.create_issue(
                "Docstring is fewer than 50 characters. Extremely cringe and undescriptivepilled",
                docstring_node
            )

        if not re.findall(r'^[\t ]+?>>> ', docstring, re.MULTILINE):
            self.create_issue(
                "NO TEST CASES????? CRIGbnre?",
                docstring_node
            )

    def visit_child_nodes(self, node: ast.AST):
        if isinstance(node, ast.Module):
            self._visit_child_nodes(node.body)
        if isinstance(node, ast.FunctionDef):
            self._visit_child_nodes(node.body)
        if isinstance(node, ast.If):
            self._visit_child_nodes(node.body)

    def _visit_node(self, node: ast.AST):
        self.on_visit_node(node)
        self.visit_child_nodes(node)

    def _visit_child_nodes(self, nodes: List):
        for node in nodes:
            self._visit_node(node)
    
    def get_line_at_lineno(self, lineno: int):
        return self.src.split("\n")[lineno-1]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("bruh no input file cringe")
        quit()

    input_file = sys.argv[1]

    with open(input_file) as fl:
        bython = BythonBTW(fl.read())

    bython.run_evaluation()

    print("Python evaluation finished: ", end="")
    if len(bython._issues):
        print(colored("{} issues detected".format(
            len(bython._issues),
        ), "red"))
    else:
        print(colored("No issues detected", "green"))

    if len(bython._issues):
        print("Issues:")

        for issue in bython._issues:
            lineno = issue.at_node.lineno
            print(colored("On line {}:".format(lineno), "yellow")+" "+colored(bython.get_line_at_lineno(lineno).strip(), "cyan"))
            print(colored("    Error: "+issue.message, "yellow"))
    
    webbrowser.open("file://"+os.path.abspath("res/cringe.html"))