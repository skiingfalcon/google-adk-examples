# ADK Bootcamp Python Project

This project contains examples and agents for the Google Agent Development Kit (ADK) bootcamp, managed with `uv` for fast dependency management.

## Setup

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate    # On Windows
   ```

3. **Set up your API key**:
   - Copy `env.example` to `.env`
   - Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Add your API key to the `.env` file

## Running Agents

### Using the ADK CLI

1. **Run the web interface**:
   ```bash
   adk web
   ```
   This will start a local server at `http://127.0.0.1:8080`

2. **Test your agent**:
   - Open the web interface in your browser
   - Try these example prompts:
     - "Hello! What's your name?"
     - "What is the main purpose of the Google Agent Development Kit?"
     - "Write a short poem about building an AI agent."
     - "Tell me a developer joke."

### Project Structure

```
adk-bootcamp-python/
├── agents/                 # Agent implementations
│   └── my_first_agent.py  # Simple agent from Lab 1
├── examples/              # Example code and utilities
│   └── simple_chat.py     # Basic chat example
├── main.py               # Main entry point
├── pyproject.toml        # Project dependencies (managed by uv)
├── env.example          # Environment variables template
└── README.md           # This file
```

## Dependencies

This project uses `uv` for fast Python package management. Key dependencies include:

- `google-adk`: Google's Agent Development Kit
- `google-cloud-aiplatform`: Google Cloud AI Platform SDK
- `google-genai`: Google Generative AI SDK

All dependencies are automatically managed by `uv` and installed in the virtual environment.

## Next Steps

1. Follow the lab instructions in the original course materials
2. Experiment with different agent configurations
3. Add custom tools and capabilities to your agents
4. Explore multi-agent systems and advanced patterns

## Troubleshooting

- **"adk command not found"**: Make sure your virtual environment is activated
- **API key errors**: Verify your `.env` file has the correct `GEMINI_API_KEY`
- **Import errors**: Ensure you're in the project directory and the virtual environment is active

