import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from dotenv import load_dotenv

from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient

# Load environment variables from .env file
load_dotenv()

# Create a test directory for the agent to access
# Get the absolute path of the directory containing this script
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Define the path for the agent's workspace
AGENT_WORKSPACE_PATH = os.path.join(_CURRENT_DIR, "agent_workspace")

# Create the directory if it doesn't exist
if not os.path.exists(AGENT_WORKSPACE_PATH):
    os.makedirs(AGENT_WORKSPACE_PATH)
    # Create a dummy file inside for the agent to find
    with open(os.path.join(AGENT_WORKSPACE_PATH, "welcome.txt"), "w") as f:
        f.write("Hello from your ADK agent's workspace!")

# Define the Filesystem Agent
root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='filesystem_agent',
    instruction=f"""
    You are a helpful assistant that can interact with a user's local file system.
    You are restricted to operate ONLY within the following directory: {AGENT_WORKSPACE_PATH}.
    Never attempt to access files or directories outside of this path.
    When a user asks you to list files, use the 'list_directory' tool.
    When a user asks you to read a file, use the 'read_file' tool.
    """,
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='npx',
                    args=[
                        "-y",  # Auto-confirm npx installation prompts
                        "@modelcontextprotocol/server-filesystem",
                        # IMPORTANT: This MUST be an absolute path.
                        AGENT_WORKSPACE_PATH,
                    ],
                ),
            ),
            # Optional: Explicitly filter which tools are exposed to the agent
            tool_filter=['list_directory', 'read_file']
        )
    ],
)


# Connect to the MCP Toolbox server (use port 7000 or whatever port you used)
toolbox = ToolboxSyncClient("http://127.0.0.1:7000")

# Load the tools from the toolset we defined in tools.yaml
tools = toolbox.load_toolset('my-toolset')

# --- Lab 2: Data Analyst Agent ---
root_agent = Agent(
    model='gemini-2.5-pro',  # Using a more powerful model for better SQL generation
    name='data_analyst_agent',
    description='Agent to answer questions about products in the database',
    instruction="""
    You are a data analyst. Your goal is to help users understand data from a
    product database. You have access to several predefined tools to query the database:

    - search-products-by-category: Search products by category (needs 'category' parameter)
    - get-products-sorted-by-price: Get products sorted by price (high to low)
    - get-low-stock-products: Get products with stock less than 200 units
    - get-average-price-by-category: Get average price for a category (needs 'category' parameter)

    The database contains products with categories: 'Electronics' and 'Home Goods'

    Use the appropriate tool based on the user's question.
    """,
    tools=tools,
)