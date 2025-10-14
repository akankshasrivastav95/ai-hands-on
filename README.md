# AI Hands-On

This repository contains experimental AI projects demonstrating various applications of artificial intelligence, from conversational agents to multi-agent systems and research automation.

## 🚀 Projects

### 1. Resume Chatbot
A conversational AI assistant that answers questions about Akanksha using information extracted from LinkedIn PDFs and personal summaries. Built with Gradio for an interactive web interface.

**Features:**
- Natural language Q&A about professional background
- PDF document processing and text extraction
- Interactive web interface

**Demo:** [Resume Chatbot (Hugging Face)](https://huggingface.co/spaces/AkankshaSrivastav/career_conversation)

**Location:** `resume/`

---

### 2. Deep Research System
An intelligent research automation platform that orchestrates multiple AI agents to conduct comprehensive research on any topic. The system generates clarifying questions, plans searches, executes web research, and produces detailed reports.

**Architecture:**
- **Product Manager Agent**: Generates clarifying questions to understand research requirements
- **Planner Agent**: Creates strategic search plans based on user responses
- **Search Agent**: Executes web searches in parallel for efficiency
- **Writer Agent**: Synthesizes findings into comprehensive reports
- **Email Agent**: Delivers final reports via email

**Features:**
- Interactive question generation and collection
- Parallel web search execution
- Comprehensive report generation with markdown formatting
- Real-time progress tracking and status updates
- Email delivery system
- Web interface with Gradio

**Key Benefits:**
- Modular, extensible agent architecture
- Error-resilient with graceful failure handling
- Real-time user feedback during research process
- Professional report formatting and delivery

**Location:** `deep-research/`

---

### 3. Engineering Team (CrewAI)
A multi-agent AI system built with CrewAI framework that demonstrates collaborative AI agents working together on complex engineering tasks. Features a trading simulation platform with account management and stock trading capabilities.

**CrewAI Features:**
- Multi-agent collaboration and task orchestration
- Configurable agents and tasks via YAML files
- Flexible framework for complex AI workflows
- Built-in support for various AI models and tools

**Trading Simulation Platform:**
- **Account Management**: Create accounts, deposit/withdraw funds
- **Stock Trading**: Buy/sell shares of AAPL, TSLA, GOOGL
- **Portfolio Tracking**: Real-time portfolio value and profit/loss calculation
- **Transaction History**: Complete audit trail of all trading activities
- **Interactive Web Interface**: User-friendly Gradio-based trading platform

**Technical Stack:**
- CrewAI framework for agent orchestration
- Gradio for web interface
- Python with type hints and modern async patterns
- UV for dependency management

**Location:** `engineering_team/`

## 🛠️ Getting Started

Each project has its own setup instructions and requirements. Navigate to the specific project directory for detailed installation and usage instructions.

### Prerequisites
- Python 3.10+ (for CrewAI projects)
- OpenAI API key (for AI agent functionality)
- Optional: SendGrid API key (for email functionality in Deep Research)

## 📁 Project Structure

```
ai-hands-on/
├── resume/                 # Resume chatbot project
├── deep-research/          # Multi-agent research system
├── engineering_team/       # CrewAI trading simulation
└── README.md              # This file
```

## 🤝 Contributing

This repository contains experimental projects for learning and demonstration purposes. Feel free to explore, modify, and extend the code for your own AI experiments.

## 📄 License

This project is for educational and experimental purposes.