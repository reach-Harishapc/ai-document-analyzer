# PDF RAG Crew 🤖📚

A powerful Retrieval-Augmented Generation (RAG) system built with CrewAI, featuring a user-friendly chat interface for intelligent document analysis and research.

![CrewAI](https://img.shields.io/badge/CrewAI-1.11.0-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

- **Intelligent Research Crew**: Multi-agent system with specialized researcher and analyst roles
- **Vector Database Integration**: Qdrant-powered semantic search for knowledge retrieval
- **Web Chat Interface**: Easy-to-use chat UI powered by CrewAI Chat UI
- **Knowledge Base Management**: Load and query custom knowledge sources
- **Comprehensive Reporting**: Generate detailed markdown reports with analysis
- **Verbose Execution**: See detailed agent interactions and reasoning
- **Human-in-the-Loop**: Optional human feedback integration for iterative refinement

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Chat UI   │────│   CrewAI Chat   │────│  Research Crew  │
│                 │    │     Interface   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Qdrant Vector  │
                    │     Database    │
                    │                 │
                    │ • Knowledge Base│
                    │ • Document Chunks│
                    │ • Semantic Search│
                    └─────────────────┘
```

### Core Components

- **Researcher Agent**: Conducts thorough research using vector search and web knowledge
- **Reporting Analyst**: Synthesizes findings into comprehensive reports
- **Qdrant Vector DB**: Stores and retrieves document embeddings for RAG
- **Sentence Transformers**: Generates embeddings for semantic search
- **CrewAI Framework**: Orchestrates multi-agent collaboration

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker (for Qdrant)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd pdf_rag
   ```

2. **Set up Python environment**
   ```bash
   # Using uv (recommended)
   pip install uv
   uv venv
   source .venv/bin/activate
   uv pip install -e .

   # Or using pip
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

3. **Start Qdrant Database**
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

4. **Configure Environment**
   ```bash
   # Copy and edit environment variables
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Load Knowledge Base**
   ```bash
   # The system automatically loads knowledge from knowledge/user_preference.txt
   # Add your documents to the knowledge/ directory
   ```

### Configuration

Edit `.env` file:
```env
MODEL=groq/llama-3.1-8b-instant
GROQ_API_KEY=your-groq-api-key
```

## 💬 Usage

### Web Chat Interface

Start the interactive chat interface:
```bash
crewai-chat-ui
```

Access at: http://localhost:4200

**Example Queries:**
- "What is in my knowledge base?"
- "Research AI LLMs for 2026"
- "Analyze the latest developments in machine learning"

### Command Line

Run the crew directly:
```bash
# Run with default inputs
python -m pdf_rag.main

# Run with custom inputs
python -c "
from pdf_rag.crew import PdfRag
crew = PdfRag().crew()
result = crew.kickoff(inputs={'topic': 'Quantum Computing', 'current_year': '2026'})
print(result)
"
```

### Programmatic Usage

```python
from pdf_rag.crew import PdfRag

# Initialize crew
crew = PdfRag().crew()

# Run research
result = crew.kickoff(inputs={
    'topic': 'Sustainable Energy',
    'current_year': '2026'
})

print(result)  # View the generated report
```

## 📁 Project Structure

```
pdf_rag/
├── src/pdf_rag/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── crew.py              # Crew definition
│   ├── config/
│   │   ├── agents.yaml      # Agent configurations
│   │   └── tasks.yaml       # Task definitions
│   └── tools/
│       └── custom_tool.py   # Qdrant integration
├── knowledge/
│   └── user_preference.txt  # Knowledge base
├── tests/
├── .env                     # Environment variables
├── pyproject.toml          # Project configuration
└── README.md
```

## ⚙️ Configuration

### Agents Configuration (`config/agents.yaml`)

```yaml
researcher:
  role: "Senior Data Researcher and Knowledge Analyst"
  goal: "Conduct thorough research and analysis on any given topic"
  backstory: "Expert researcher with access to vector databases and web knowledge"

reporting_analyst:
  role: "Senior Reporting Analyst and Content Specialist"
  goal: "Create detailed, well-structured reports and analysis"
  backstory: "Meticulous analyst skilled in synthesizing complex information"
```

### Tasks Configuration (`config/tasks.yaml`)

```yaml
research_task:
  description: "Conduct comprehensive research on the given topic"
  expected_output: "Detailed research summary with multiple insights"
  agent: researcher

reporting_task:
  description: "Create comprehensive report from research findings"
  expected_output: "Well-structured markdown report with analysis"
  agent: reporting_analyst
```

## 🔧 Advanced Features

### Knowledge Base Management

Add documents to the `knowledge/` directory:
```bash
# Text files are automatically loaded into Qdrant
echo "Your knowledge content here" > knowledge/new_document.txt
```

### Custom Tools

Extend functionality by adding tools in `tools/custom_tool.py`:
```python
def custom_analysis_tool(query: str) -> str:
    # Your custom analysis logic
    return f"Analysis result for: {query}"
```

### Human-in-the-Loop

Enable human feedback in tasks:
```python
@task
@human_feedback
def research_task(self) -> Task:
    return Task(config=self.tasks_config['research_task'])
```

## 🐛 Troubleshooting

### Common Issues

1. **"Empty string response from LLM"**
   - Check your API keys in `.env`
   - Verify the model is available (try `groq/llama-3.1-8b-instant`)

2. **"No module named 'pdf_rag'"**
   - Run `pip install -e .` to install the package
   - Check PYTHONPATH includes the src directory

3. **Qdrant connection failed**
   - Ensure Docker is running: `docker run -p 6333:6333 qdrant/qdrant`
   - Check Qdrant is accessible at `http://localhost:6333`

4. **Import errors**
   - Activate virtual environment: `source .venv/bin/activate`
   - Install dependencies: `uv pip install -e .`

### Debug Mode

Enable verbose logging:
```bash
PYTHONPATH=src:$PYTHONPATH LITELLM_LOG=DEBUG crewai-chat-ui
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://crewai.com) - Multi-agent framework
- [Qdrant](https://qdrant.tech) - Vector database
- [Sentence Transformers](https://sbert.net) - Embedding models
- [Groq](https://groq.com) - Fast LLM inference

## 📞 Support

- **Documentation**: [CrewAI Docs](https://docs.crewai.com)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)

---

**Built with ❤️ using CrewAI**
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
