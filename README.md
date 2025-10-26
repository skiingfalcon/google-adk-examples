# Google ADK Samples

A comprehensive collection of examples and agents demonstrating the capabilities of the Google Agent Development Kit (ADK). This repository showcases various agent patterns, tools, and integrations for building intelligent AI agents.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) for fast dependency management

### Setup

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and setup the project**:
   ```bash
   git clone https://github.com/skiingfalcon/google-adk-examples.git
   cd google-adk-examples
   uv sync
   ```

3. **Set up your API key**:
   - Copy `env.example` to `.env`
   - Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Add your API key to the `.env` file

4. **Run an agent**:
   ```bash
   adk web
   ```
   This will start a local server at `http://127.0.0.1:8080`

## 📁 Project Structure

This repository contains multiple agent examples organized by functionality and complexity:

### 🤖 Core Agent Examples

#### **Basic Agents**
- **`my_first_agent/`** - Simple introductory agent demonstrating basic ADK concepts
- **`model_agent/`** - Agent showcasing different model configurations and capabilities

#### **Specialized Domain Agents**
- **`data_agent/`** - BigQuery integration agent for data analysis and querying
- **`news_agent/`** - Financial news agent with real-time stock data and Google Search integration
- **`shopping_agent/`** - Shopping list management agent with state persistence
- **`petstore_agent/`** - E-commerce agent demonstrating API interactions

### 🔧 Advanced Agent Patterns

#### **Agent-to-Agent (A2A) Communication**
- **`a2a_adk/`** - Demonstrates agent-to-agent communication patterns
  - `agent.py` - Orchestrator agent that coordinates with remote math service
  - `math_agent.py` - Specialized math calculation agent

#### **Multi-Agent Systems**
- **`adk-multiagent-lab/`** - Comprehensive multi-agent patterns:
  - **`coordinator_pattern/`** - Coordinator agent managing specialist agents (billing, support, sales)
  - **`sequential_pattern/`** - Sequential agent workflow patterns
  - **`parallel_pattern/`** - Parallel agent execution patterns
  - **`loop_pattern/`** - Iterative agent processing patterns
  - **`human_loop_pattern/`** - Human-in-the-loop agent workflows
  - **`hierarchical_pattern/`** - Hierarchical agent organization

#### **Memory-Enabled Agents**
- **`my_agent_with_memory/`** - Demonstrates persistent memory capabilities
  - `memory_lab.py` - Memory service integration with conversation persistence
  - `run_agent.py` - Example of running memory-enabled agents

#### **Field Notebook Agent**
- **`field_notebook/`** - Agent with artifact management capabilities for saving and retrieving files

### 🛡️ Security & Analysis

#### **Prompt Security Agent**
- **`prompt_security_agent/`** - Advanced security analysis agent with multi-agent architecture:
  - **Scanner Agent** - Identifies and extracts prompts from code files using AST analysis
  - **Analyzer Agent** - Analyzes prompts for security vulnerabilities (injection, data leakage, etc.)
  - **Reporter Agent** - Generates comprehensive security reports
  - **Features**: Semgrep integration, vulnerability detection, detailed reporting

### 🔌 Integration Examples

#### **Model Context Protocol (MCP)**
- **`adk-mcp-lab/`** - MCP integration examples:
  - `adk_mcp_agent/` - Agent with MCP toolset integration
  - `mcp-toolbox/` - MCP toolbox configuration and tools
  - `products.db` - Sample database for MCP operations

#### **Custom Agent Lab**
- **`adk-custom-agent-lab/`** - Custom agent development examples:
  - `creative_writing_agent/` - Specialized creative writing agent

### 📚 Utilities & Examples
- **`examples/`** - Basic usage examples and utilities
- **`main.py`** - Project entry point and overview

## 🛠️ Key Dependencies

This project uses modern Python tooling and Google's latest AI services:

- **`google-adk[a2a]`** - Google Agent Development Kit with A2A support
- **`google-cloud-bigquery`** - BigQuery integration for data agents
- **`toolbox-core`** - MCP toolbox core functionality
- **`yfinance`** - Financial data integration
- **`semgrep`** - Security analysis (optional)
- **`bandit`** - Security linting (optional)

## 🎯 Usage Examples

### Running Individual Agents

```bash
# Start the web interface
adk web

# Test with example prompts:
# - "Hello! What's your name?"
# - "What is the main purpose of the Google Agent Development Kit?"
# - "Write a short poem about building an AI agent."
# - "Tell me a developer joke."
```

### Running Specific Agent Types

```bash
# Run the memory lab example
cd my_agent_with_memory
python run_agent.py

# Run the prompt security analysis
cd prompt_security_agent
python run_example.py

# Run the data agent with BigQuery
cd data_agent
python agent.py
```

## 🔒 Security Features

- **Environment Variables**: All API keys stored in `.env` files (ignored by git)
- **Prompt Security**: Advanced vulnerability detection and analysis
- **Code Analysis**: AST-based prompt extraction and security scanning
- **Report Generation**: Comprehensive security reports with remediation suggestions

## 🚀 Advanced Features

### Multi-Agent Coordination
- **Coordinator Pattern**: Central agent managing specialist agents
- **Sequential Processing**: Chain agents for complex workflows
- **Parallel Execution**: Run multiple agents simultaneously
- **Human-in-the-Loop**: Interactive agent workflows

### Memory & Persistence
- **Session Memory**: Conversation persistence across interactions
- **Artifact Management**: File saving and retrieval capabilities
- **State Management**: Persistent agent state across sessions

### Integration Capabilities
- **BigQuery**: Direct database querying and analysis
- **Google Search**: Real-time web search integration
- **Financial Data**: Stock market data integration
- **MCP Protocol**: Model Context Protocol for tool integration

## 🐛 Troubleshooting

- **"adk command not found"**: Make sure your virtual environment is activated
- **API key errors**: Verify your `.env` file has the correct `GEMINI_API_KEY`
- **Import errors**: Ensure you're in the project directory and the virtual environment is active
- **Large file errors**: The repository excludes large binary files via `.gitignore`

## 📖 Learning Path

1. **Start with**: `my_first_agent/` for basic concepts
2. **Explore**: `model_agent/` for different model configurations
3. **Try**: `shopping_agent/` for state management
4. **Advance to**: Multi-agent patterns in `adk-multiagent-lab/`
5. **Master**: Security analysis with `prompt_security_agent/`

## 🤝 Contributing

This repository serves as a comprehensive reference for Google ADK development. Feel free to:
- Explore the different agent patterns
- Experiment with custom configurations
- Add new agent examples
- Improve existing implementations

## 📄 License

This project contains examples and educational materials for the Google Agent Development Kit. Please refer to Google's licensing terms for the ADK components.

---

**Ready to build intelligent agents? Start with `adk web` and explore the examples!** 🚀