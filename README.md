# Aletheia - Cognitive Ecosystem for Market Intelligence

Aletheia is an advanced AI-powered platform that operates as an ecosystem of autonomous agents for market intelligence and alpha generation. The system collects, processes, analyzes, correlates, and synthesizes information from a wide spectrum of textual and quantitative sources to identify market narratives, detect anomalies, assess risks, and generate actionable insights.

![Aletheia Platform](https://github.com/lucas-blue3/News-Telegram-Finance/raw/main/docs/images/aletheia_dashboard.png)

## Architecture

Aletheia is modeled as a team of investment fund analysts, managed with LangGraph to enable cyclical, collaborative, and self-correcting workflows:

1. **Strategist Agent (CIO)**: The main entry point that receives high-level directives and decomposes them into strategic plans.
2. **Orchestrator Agent**: Manages the flow of data collection and initial processing, invoking hunter and analyst agents efficiently.
3. **Specialist Agents**:
   - **Narrative Hunter**: Collects qualitative data from Twitter, news sources, SEC filings, research articles, and social media.
   - **Quantitative Analyst**: Gathers quantitative data from financial APIs and economic indicators.
   - **Intelligence Analyst**: Performs advanced sentiment analysis, extracts causal relationships, identifies market narratives, and creates persona-specific summaries.
   - **Risk Analyst**: Challenges the main narrative, finds contradictory evidence, identifies black swan signals, and assesses geopolitical risk factors.

## Technology Stack

- **Cognitive Engine**: DeepSeek API
- **Orchestration**: LangChain and LangGraph
- **Memory**:
  - Short-term: ConversationBufferWindowMemory
  - Long-term: Vector Database (ChromaDB/FAISS)
- **Structured Knowledge Base**:
  - Relational Database (PostgreSQL/SQLite)
  - (Optional) Graph Database (Neo4j)
- **Interface**: Interactive Streamlit Dashboard with Plotly visualizations

## Getting Started

### Prerequisites

- Python 3.10+
- Docker and Docker Compose (for containerized deployment)

### Quick Start

The easiest way to get started is to use the installation script:

```bash
# Make the script executable
chmod +x install_and_run.sh

# Run the installation script
./install_and_run.sh
```

This will:
1. Create a virtual environment
2. Install all dependencies
3. Run the Streamlit app

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lucas-blue3/News-Telegram-Finance.git
   cd News-Telegram-Finance
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

   You'll need to obtain the following API keys:
   - **DeepSeek API**: Sign up at [DeepSeek](https://deepseek.ai/) to get your API key
   - **Twitter/X API**: Create a developer account at [Twitter Developer Portal](https://developer.twitter.com/)
   - **Tavily API**: Register at [Tavily](https://tavily.com/) for web search and news capabilities
   - **FRED API**: Get your API key from [FRED (Federal Reserve Economic Data)](https://fred.stlouisfed.org/docs/api/api_key.html)

   > **SECURITY WARNING**: Never commit your `.env` file to version control. It's already added to `.gitignore` to prevent accidental exposure of your API keys. If you accidentally committed API keys, consider them compromised and rotate them immediately.
   
   Example `.env` file format:
   ```
   # API Keys
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   DEEPSEEK_API_BASE_URL=https://api.deepseek.com/v1
   
   # Twitter/X API
   TWITTER_API_KEY=your_twitter_api_key_here
   TWITTER_API_SECRET=your_twitter_api_secret_here
   TWITTER_ACCESS_TOKEN=your_twitter_access_token_here
   TWITTER_ACCESS_SECRET=your_twitter_access_secret_here
   TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
   
   # Tavily API (for news and web search)
   TAVILY_API_KEY=your_tavily_api_key_here
   
   # FRED API
   FRED_API_KEY=your_fred_api_key_here
   
   # Database Configuration
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_secure_password_here
   POSTGRES_DB=aletheia
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   
   # Vector Database
   VECTOR_DB_PATH=./data/vectordb
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -e .
   ```

5. Run the application:
   ```bash
   python run_app.py
   ```

### Docker Deployment

```bash
docker-compose -f docker/docker-compose.yml up -d
```

## Usage

1. Access the Streamlit dashboard at http://localhost:12000
2. Use the chat interface to interact with the Strategist Agent
3. View generated insights, visualizations, and reports

## Project Structure

```
aletheia/
├── agents/                 # Agent implementations
│   ├── strategist.py       # CIO agent
│   ├── orchestrator.py     # Operations agent
│   ├── hunters/            # Data collection agents
│   └── analysts/           # Analysis agents
├── tools/                  # Specialized tools for agents
├── memory/                 # Memory implementations
├── api/                    # API connectors
├── graphs/                 # LangGraph implementations
└── ui/                     # Streamlit dashboard
    └── components/         # UI components
```

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Adding New Features

1. Implement new agents in the `aletheia/agents/` directory
2. Add new tools in the `aletheia/tools/` directory
3. Update the orchestration graph in `aletheia/graphs/` directory
4. Add new UI components in the `aletheia/ui/components/` directory

## License

[MIT License](LICENSE)

## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain) for the agent framework
- [LangGraph](https://github.com/langchain-ai/langgraph) for the orchestration framework
- [Streamlit](https://streamlit.io/) for the interactive dashboard
- [Plotly](https://plotly.com/) for the visualizations
- [DeepSeek](https://deepseek.ai/) for the cognitive engine