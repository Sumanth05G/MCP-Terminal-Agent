from fastmcp import FastMCP
import subprocess
import os

mcp = FastMCP("TerminalServer")

@mcp.tool()
def execute_linux_command(command: str, directory: str) -> str:
    """Executes a shell command in a specific directory."""
    try:
        # Standard subprocess execution
        result = subprocess.run(
            command, shell=True, cwd=os.path.abspath(directory),
            capture_output=True, text=True, timeout=30
        )
        return f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")