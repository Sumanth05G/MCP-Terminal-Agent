# MCP-Terminal-Agent
A secure, natural-language terminal assistant that connects Google's Gemini models to your local shell using the Model Context Protocol (MCP)


This project is a proof-of-concept AI agent that bridges the gap between natural language reasoning and local system execution. It leverages **Google's Gemini 2.5 Flash** model to interpret user intent and uses the **Model Context Protocol (MCP)** to standardize how the AI interfaces with local tools.

Unlike standard "text-to-cmd" generators, this project implements a full **Client-Server architecture**:

1. **The Agent (Client):** Handles the LLM lifecycle, manages the conversation context, and acts as a security gatekeeper.
2. **The Server (MCP):** A dedicated subprocess (built with `fastmcp`) that exposes specific capabilities (like executing shell commands) in a sandboxed, modular way.

**Key Features:**

* **Natural Language Control:** Execute complex Linux commands by simply asking in plain English (e.g., *"Find all Python files modified yesterday and list their sizes"*).
* **Human-in-the-Loop Security:** Critical safety mechanism that intercepts every AI-generated command. The user must explicitly approve the action and path before execution, preventing hallucinated `rm -rf` disasters.
* **Model Context Protocol (MCP) Implementation:** Uses the official `mcp-python-sdk` to establish a robust `stdio` transport layer between the AI reasoning engine and the execution environment.
* **Gemini Integration:** Updated to support the latest Google Generative AI models for faster inference and better tool-calling accuracy.

**Tech Stack:**

* **Language:** Python 3.13+
* **AI Model:** Google Gemini 2.5 Flash (`google-generativeai`)
* **Protocol:** Model Context Protocol (`mcp`, `fastmcp`)
* **Concurrency:** Asyncio for non-blocking I/O

**How it Works:**

1. User inputs a request ("Check my disk usage").
2. Agent sends the prompt + tool definitions to Gemini.
3. Gemini reasons that it needs to run `df -h` and returns a **Function Call**.
4. Agent intercepts the call and prompts the user: `[PERMISSION REQUEST] Run 'df -h'? (y/n)`.
5. Upon approval, the Agent sends the command to the MCP Server via the `stdio` connection.
6. MCP Server executes the command via `subprocess` and returns `STDOUT`/`STDERR`.
7. Agent displays the execution's output to the user.


<img width="1347" height="1002" alt="Screenshot From 2026-01-07 10-32-08" src="https://github.com/user-attachments/assets/29bcf769-517c-4924-b383-22dc2a406e91" />
