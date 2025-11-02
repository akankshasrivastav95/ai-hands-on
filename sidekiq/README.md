# Sidekick - Personal AI Co-Worker

Sidekick is an intelligent AI assistant that autonomously completes tasks using a self-evaluating workflow. Built with LangGraph, it features a worker-evaluator architecture that continuously refines its work until success criteria are met.

## 🤖 Overview

Sidekick is designed to be your personal co-worker that can handle complex, multi-step tasks independently. It uses a sophisticated feedback loop where a worker agent performs actions and an evaluator agent assesses whether the work meets your specified success criteria. If the criteria aren't met, the worker iteratively improves based on feedback until the task is complete.

## ✨ Features

### Core Capabilities
- **Autonomous Task Execution**: Works independently on tasks until completion
- **Self-Evaluation**: Built-in evaluator ensures quality and completeness
- **Iterative Improvement**: Automatically refines work based on feedback
- **Interactive Web Interface**: User-friendly Gradio interface for easy interaction

### Available Tools
Sidekick has access to a comprehensive toolkit:

- **🌐 Web Browsing**: Navigate and interact with web pages using Playwright
- **🔍 Web Search**: Search the internet using Google Serper API
- **📚 Wikipedia**: Query Wikipedia for information
- **📁 File Management**: Read, write, and manage files in the sandbox directory
- **🐍 Python REPL**: Execute Python code for data processing and calculations
- **📱 Push Notifications**: Send notifications (requires Pushover credentials)

## 🏗️ Architecture

### Worker-Evaluator Loop

Sidekick uses a LangGraph-based workflow with three main components:

1. **Worker Agent**: Performs actions using available tools to complete your request
2. **Evaluator Agent**: Assesses the worker's output against your success criteria
3. **Router Logic**: Determines whether to continue working, use tools, or finish

### Workflow
```
User Request → Worker Agent → Tools (if needed) → Evaluator Agent
                                      ↑                    ↓
                                      └──── Feedback Loop ─┘
```

The worker continues iterating until either:
- Success criteria are met
- The agent needs user clarification
- The agent determines it cannot proceed without help

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- OpenAI API key
- Google Serper API key (for web search)
- Pushover credentials (optional, for notifications)

### Installation

1. Ensure you're in the project root directory
2. Install Playwright browsers:
   ```bash
   uv run playwright install chromium
   ```

### Running Sidekick

From the `sidekiq` directory:

```bash
uv run app.py
```

This will launch the Gradio web interface, which opens automatically in your browser.

## 💻 Usage

1. **Enter Your Request**: Type your task or question in the message box
2. **Define Success Criteria**: Specify what "success" means for your task (e.g., "Generate a summary report with key findings")
3. **Click Go!**: Sidekick will start working on your task
4. **Review Results**: Watch as Sidekick works through the task and evaluates its progress

### Example Requests

- "Research the latest developments in AI and create a summary report"
- "Write a Python script that analyzes stock market data"
- "Find information about renewable energy and create a markdown file with your findings"

## 📁 Output Files

**Important**: If Sidekick writes any output files (documents, scripts, reports, etc.), they will be saved in the **`sandbox/`** folder within the sidekiq directory.

The `sandbox/` folder serves as the working directory for all file operations. Check this folder to find:
- Generated reports and documents
- Created Python scripts
- Any other files Sidekick creates during task execution

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root with:

```env
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
PUSHOVER_TOKEN=your_pushover_token  # Optional
PUSHOVER_USER=your_pushover_user    # Optional
```

## 🛠️ Technical Details

### Built With
- **LangGraph**: Workflow orchestration and state management
- **LangChain**: LLM integration and tool abstractions
- **OpenAI GPT-4o-mini**: Language model for both worker and evaluator
- **Playwright**: Web browser automation
- **Gradio**: Web interface framework

### Key Components

- `sidekiq.py`: Core Sidekick class with worker-evaluator logic and LangGraph workflow
- `sidekiq_tools.py`: Tool definitions and configurations
- `app.py`: Gradio web interface and application entry point

## 🎯 Success Criteria

Defining clear success criteria helps Sidekick understand when a task is complete. Examples:

- "Create a 500-word summary with at least 3 key points"
- "Generate a working Python script with error handling"
- "Provide a detailed answer with citations"
- "Create a markdown file with formatted content"

## 🔄 Reset and Cleanup

Use the "Reset" button to:
- Clear the conversation history
- Start a new session with a fresh Sidekick instance
- Clean up browser and Playwright resources

## 📝 Notes

- Sidekick runs the browser in non-headless mode by default for better debugging
- Each Sidekick instance maintains its own conversation state
- The evaluator gives the worker the "benefit of the doubt" when assessing completion
- If Sidekick needs clarification, it will explicitly ask questions

## 🤝 Contributing

This is an experimental project. Feel free to explore, modify, and extend the functionality.

