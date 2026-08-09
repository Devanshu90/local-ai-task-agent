# Local AI Task Agent

A local agentic AI assistant built with Python, Ollama, and Qwen3.

This project demonstrates how a Large Language Model (LLM) can autonomously select and execute tools, perform multi-step tasks, maintain long-term memory, search the web, and execute Python code.

## Features

- Local LLM inference using Ollama
- Qwen3 4B model
- LLM tool calling
- Multi-step agentic execution loop
- Calculator tool
- Safe workspace-based file operations
- File creation and reading
- Folder creation
- Long-term memory using SQLite
- Web search using DDGS
- Python code execution
- Continuous conversational interaction
- Maximum-step protection against infinite tool loops

## Architecture

text
                         User
                           |
                           v
                    +-------------+
                    |    Qwen3    |
                    |   Local LLM |
                    +------+------+
                           |
                    Decide next action
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
     Calculator       File Tools       Web Search
          |                |                |
          |                v                |
          |           Workspace             |
          |                                 |
          +----------------+----------------+
                           |
                           v
                    Tool Result
                           |
                           v
                        Qwen3
                           |
                    Need another tool?
                       /       \
                     Yes        No
                      |          |
                      v          v
                    Tool      Final Answer

Tech Stack
Python 3.13
Ollama
Qwen3 4B
SQLite
DDGS
Git & GitHub
Project Structure
simple_agent/
│
├── agent.py              # Main agent and tool-calling loop
├── tools.py              # Agent tools
├── memory.py             # SQLite long-term memory
├── README.md             # Project documentation
├── .gitignore            # Ignored files
│
└── workspace/            # Agent-controlled file workspace\

Current Tools
Calculator
Performs mathematical calculations.
File Creation
The agent can create files inside the controlled workspace.
File Reading
The agent can read files from the workspace.
Folder Creation
The agent can create folders inside the workspace.
Web Search
The agent can search the web when current or online information is required.
Python Execution
The agent can execute Python code for tasks such as calculations, data processing, and experimentation.
Long-Term Memory
The agent uses SQLite to store information across sessions.

Agentic Workflow

The agent follows an iterative tool-use loop:
User Task
    |
    v
Qwen3
    |
    v
Select Tool
    |
    v
Execute Tool
    |
    v
Observe Result
    |
    v
Qwen3
    |
    +----> Another Tool
    |
    v
Final Answer
The agent is limited to a maximum number of steps to prevent infinite tool-calling loops.

Installation

1. Install Ollama
2. Download Qwen3
3. Install Python Dependencies : py -m pip install ollama ddgs

Safety
The agent's file operations are restricted to the workspace directory.
Attempts to access files outside the workspace are rejected.
Python execution includes several restrictions:
Runs in a separate Python process
Uses the workspace as its working directory
Has a 10-second execution timeout
Does not invoke a shell
Uses Python isolated mode
However, these measures do not constitute a complete security sandbox. Python execution should not be treated as safe for arbitrary untrusted code.

Future Improvements

Better task planning
Task decomposition
Improved memory retrieval
Memory summarization
Human approval for dangerous actions
More tools
Better Python sandboxing
Agent evaluation and benchmarks
Streamlit web interface
GUI for monitoring agent actions
Logging and observability
Multiple specialized agents

Learning Goals

This project is being developed to understand:
Large Language Models
Agentic AI
Function/tool calling
Agent loops
Memory systems
Retrieval
Planning
Autonomous task execution
AI safety and permissions
