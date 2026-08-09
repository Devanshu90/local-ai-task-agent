from ollama import chat

from tools import (
    calculator,
    create_file,
    read_file,
    list_files,
    create_folder,
    web_search,
    run_python,
    save_memory,
    recall_memory,
    list_memories
)

MODEL = "qwen3:4b"
MAX_STEPS = 10
DEBUG = False

# ============================================================
# TOOL REGISTRY
# ============================================================

available_tools = {

    "calculator": calculator,

    "create_file": create_file,

    "read_file": read_file,

    "list_files": list_files,

    "create_folder": create_folder,

    "web_search": web_search,

    "run_python": run_python,

    "save_memory": save_memory,

    "recall_memory": recall_memory,

    "list_memories": list_memories
}


tools = list(
    available_tools.values()
)


# ============================================================
# TOOL EXECUTION
# ============================================================

def execute_tool(
    tool_name,
    arguments
):

    function = available_tools.get(
        tool_name
    )

    if function is None:

        return (
            f"Unknown tool: {tool_name}"
        )

    try:

        result = function(
            **arguments
        )

        return str(result)

    except Exception as e:

        return (
            f"Tool execution error: {e}"
        )


# ============================================================
# AGENT
# ============================================================

def run_agent(
    user_input,
    messages
):

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    for step in range(
        MAX_STEPS
    ):

        if DEBUG:
            print(
                f"\n--- Agent step {step + 1} ---"
            )

        response = chat(

            model=MODEL,

            messages=messages,

            tools=tools,

            think=False
        )

        messages.append(
            response.message
        )

        # ----------------------------------------------------
        # No tool required
        # ----------------------------------------------------

        if not response.message.tool_calls:

            print(
                "\nAgent:",
                response.message.content.strip()
            )

            return

        # ----------------------------------------------------
        # Execute tools
        # ----------------------------------------------------

        for tool_call in (
            response.message.tool_calls
        ):

            tool_name = (
                tool_call.function.name
            )

            arguments = (
                tool_call.function.arguments
            )

            if DEBUG:

                print(
                    f"Tool: {tool_name}"
                )

                print(
                    f"Arguments: {arguments}"
                )

            result = execute_tool(
                tool_name,
                arguments
            )

            if DEBUG:

                print(
                    f"Result: {result}"
                )

            messages.append(
                {
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": result
                }
            )

    if DEBUG:

        print(
            "\nAgent stopped: "
            "maximum steps reached."
        )

# ============================================================
# MAIN CHAT
# ============================================================

def main():

    messages = [

        {
            "role": "system",

            "content": (
                "You are an autonomous local task agent. "

                "You can use tools to accomplish tasks. "

                "Use calculator for mathematics. "

                "Use file tools for workspace files. "

                "Use web_search when the user asks "
                "for current or online information. "

                "Use run_python when actual Python "
                "execution is useful. "

                "Use save_memory when the user explicitly "
                "asks you to remember something. "

                "Use recall_memory when previous user "
                "information would help. "

                "Use list_memories when you need to inspect "
                "stored memories. "

                "All file operations are restricted "
                "to the workspace. "

                "You may use multiple tools. "

                "Continue until the user's task is complete. "

                "Do not show your reasoning or internal thoughts. "

                "Only provide the final answer to the user. "

                "Keep final answers concise."
            )
        }
    ]

    print(
    "\n" + "=" * 40
    )

    print(
    "       LOCAL AI TASK AGENT"
    )

    print(
    "=" * 40
    )

    print(
    f"Model: {MODEL}"
    )

    print(
    f"Debug: {'ON' if DEBUG else 'OFF'}"
    )

    print(
    "\nType 'exit' to quit."
    )

    while True:

        try:

            user_input = input(
                "\nYou: "
            )

        except KeyboardInterrupt:

            print(
                "\n\nGoodbye!"
            )

            break


        if user_input.lower().strip() in (
            "exit",
            "quit"
        ):

            print(
                "\nGoodbye!"
            )

            break


        if not user_input.strip():

            continue


        run_agent(
            user_input,
            messages
        )


if __name__ == "__main__":

    main()