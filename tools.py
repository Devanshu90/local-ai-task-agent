import ast
import math
import os
import subprocess
import sys

from ddgs import DDGS

from memory import (
    save_memory,
    recall_memory,
    list_memories
)


WORKSPACE = os.path.abspath("workspace")


os.makedirs(WORKSPACE, exist_ok=True)


# ============================================================
# CALCULATOR
# ============================================================

ALLOWED_OPERATORS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.FloorDiv: lambda a, b: a // b,
    ast.Mod: lambda a, b: a % b,
    ast.Pow: lambda a, b: a ** b,
}


def evaluate_math(node):

    if isinstance(node, ast.Expression):
        return evaluate_math(node.body)

    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Invalid value.")

    if isinstance(node, ast.UnaryOp):

        value = evaluate_math(node.operand)

        if isinstance(node.op, ast.USub):
            return -value

        if isinstance(node.op, ast.UAdd):
            return value

        raise ValueError("Invalid unary operator.")

    if isinstance(node, ast.BinOp):

        left = evaluate_math(node.left)
        right = evaluate_math(node.right)

        operator = ALLOWED_OPERATORS.get(type(node.op))

        if operator is None:
            raise ValueError("Operator not allowed.")

        return operator(left, right)

    raise ValueError("Invalid mathematical expression.")


def calculator(expression):
    try:

        tree = ast.parse(
            expression,
            mode="eval"
        )

        result = evaluate_math(tree)

        return str(result)

    except Exception as e:

        return f"Calculator error: {e}"


# ============================================================
# FILE TOOLS
# ============================================================

def get_safe_path(filename):

    path = os.path.abspath(
        os.path.join(
            WORKSPACE,
            filename
        )
    )

    if not (
        path == WORKSPACE
        or path.startswith(WORKSPACE + os.sep)
    ):

        raise ValueError(
            "Access outside workspace is not allowed."
        )

    return path


def create_file(filename, content):

    try:

        path = get_safe_path(filename)

        parent_directory = os.path.dirname(path)

        os.makedirs(
            parent_directory,
            exist_ok=True
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content)

        return (
            f"File '{filename}' "
            f"created successfully."
        )

    except Exception as e:

        return f"File creation error: {e}"


def read_file(filename):

    try:

        path = get_safe_path(filename)

        if not os.path.exists(path):

            return (
                f"File '{filename}' "
                f"does not exist."
            )

        if not os.path.isfile(path):

            return (
                f"'{filename}' "
                f"is not a file."
            )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        return content

    except Exception as e:

        return f"File reading error: {e}"


def list_files():

    try:

        files = []

        for root, directories, filenames in os.walk(
            WORKSPACE
        ):

            for filename in filenames:

                full_path = os.path.join(
                    root,
                    filename
                )

                relative_path = os.path.relpath(
                    full_path,
                    WORKSPACE
                )

                files.append(relative_path)

        if not files:

            return "Workspace is empty."

        return "\n".join(files)

    except Exception as e:

        return f"Error listing files: {e}"


def create_folder(foldername):

    try:

        path = get_safe_path(foldername)

        os.makedirs(
            path,
            exist_ok=True
        )

        return (
            f"Folder '{foldername}' "
            f"created successfully."
        )

    except Exception as e:

        return f"Folder creation error: {e}"


# ============================================================
# WEB SEARCH
# ============================================================

def web_search(query, max_results=5):

    try:

        max_results = min(
            int(max_results),
            8
        )

        results = DDGS().text(
            query,
            max_results=max_results
        )

        if not results:

            return "No search results found."

        output = []

        for index, result in enumerate(
            results,
            start=1
        ):

            title = result.get(
                "title",
                "No title"
            )

            url = result.get(
                "href",
                ""
            )

            body = result.get(
                "body",
                ""
            )

            output.append(
                f"{index}. {title}\n"
                f"URL: {url}\n"
                f"Summary: {body}"
            )

        return "\n\n".join(output)

    except Exception as e:

        return f"Web search error: {e}"


# ============================================================
# PYTHON EXECUTION
# ============================================================

def run_python(code):

    try:

        result = subprocess.run(
            [
                sys.executable,
                "-I",
                "-c",
                code
            ],
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=10,
            shell=False
        )

        output = result.stdout

        if result.stderr:

            output += (
                "\nERROR:\n"
                + result.stderr
            )

        if not output:

            output = (
                "Python executed successfully "
                "with no output."
            )

        return output

    except subprocess.TimeoutExpired:

        return (
            "Python execution stopped: "
            "10 second timeout."
        )

    except Exception as e:

        return f"Python execution error: {e}"