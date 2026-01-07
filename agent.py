import sys
import asyncio
import os
import google.generativeai as genai

# Import the official MCP client components
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession

# 1. Setup LLM
genai.configure(api_key="Gemini api key")

# Tool definition for Gemini
def execute_linux_command(command: str, directory: str):
    """Executes a shell command in a specific directory."""
    pass

async def main():
    # 2. Define Server Parameters
    server_params = StdioServerParameters(
        command=sys.executable, 
        args=["mcp_server.py"], 
        env=os.environ.copy()
    )

    print("Connecting to MCP Server...")

    # 3. Establish the connection using the native MCP SDK
    # stdio_client manages the process streams
    async with stdio_client(server_params) as (read, write):
        # ClientSession manages the MCP protocol
        async with ClientSession(read, write) as session:
            # Initialize the session (handshake)
            await session.initialize()
            
            # Setup Gemini
            model = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                tools=[execute_linux_command] 
            )

            user_input = input("\nWhat should I do in the terminal?\n> ")
            while user_input != "exit":
                # 4. Generate response
                response = model.generate_content(user_input)

                # 5. Check for function call
                if (response.candidates and 
                    response.candidates[0].content.parts and 
                    response.candidates[0].content.parts[0].function_call):
                    
                    call = response.candidates[0].content.parts[0].function_call
                    cmd = call.args.get('command')
                    path = call.args.get('directory', os.getcwd())

                    # 6. HUMAN-IN-THE-LOOP
                    print(f"\n--- [PERMISSION REQUEST] ---")
                    print(f"Action: {cmd}\nPath: {path}")
                    confirm = input("Confirm execution? (y/n): ")

                    if confirm.lower() == 'y':
                        # Call the tool via the active session
                        result = await session.call_tool(
                            "execute_linux_command", 
                            arguments={"command": cmd, "directory": path}
                        )
                        
                        # Parse standard MCP result format
                        # result.content is a list of TextContent or ImageContent
                        output_text = ""
                        if result.content:
                            for item in result.content:
                                if hasattr(item, 'text'):
                                    output_text += item.text

                        print(f"\n[OUTPUT]:\n{output_text}")
                    else:
                        print("Execution denied by user.")
                else:
                    print(f"Agent: {response.text}")
                user_input = input("\nWhat should I do in the terminal?\n> ")

if __name__ == "__main__":
    asyncio.run(main())