# ⚗️ ContentAlchemy — AI Content Marketing Assistant

A production-ready multi-agent content marketing assistant built with **LangGraph**, **Claude Sonnet 4.6**, **Tavily AI**, and **DALL-E 3**.

---

## Architecture Overview

```
User Input
    │
    ▼
┌─────────────────┐
│  Query Handler  │  ← Routes intent using Claude
└────────┬────────┘
         │ conditional routing
    ┌────┴──────────────────────────────────┐
    │                                       │
    ▼                                       ▼
┌──────────────┐                   ┌────────────────────┐
│ Research     │                   │  LinkedIn Writer   │
│ Agent        │                   │  Image Generator   │
│ (Tavily+     ├──────────────────►│  Content           │
│  Claude)     │ blog/strategy     │  Strategist        │
└──────────────┘                   └────────────────────┘
    │ blog
    ▼
┌──────────────┐
│  Blog Writer │  ← SEO-optimized with research context
└──────────────┘
```

### The 6 Agents

| Agent | Route | What it does |
|-------|-------|-------------|
| **Query Handler** | entry | Analyzes intent, extracts topic/audience/tone, routes to correct agent |
| **Research Agent** | `research` | Searches web via Tavily, synthesizes findings with Claude |
| **Blog Writer** | `blog` | Creates 800-1500 word SEO blog post, includes quality & SEO scoring |
| **LinkedIn Writer** | `linkedin` | Writes engagement-optimized posts with hashtag strategy |
| **Image Generator** | `image` | Optimizes prompt with Claude, generates image with DALL-E 3 |
| **Content Strategist** | `strategy` | Builds 4-week content strategy brief from research |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Claude Sonnet 4.6 (Anthropic) |
| Orchestration | LangGraph with MemorySaver |
| Research | Tavily AI (advanced search) |
| Image Generation | DALL-E 3 (OpenAI) |
| Web Interface | Streamlit |
| Config | Pydantic Settings + python-dotenv |

---

## Setup

### 1. Clone and install dependencies

```bash
cd ContentAlchemy
pip install -r requirements.txt
```

### 2. Configure API keys

```bash
cp .env.example .env
```

Edit `.env` and add your keys:

```env
ANTHROPIC_API_KEY=sk-ant-...       # https://console.anthropic.com/
TAVILY_API_KEY=tvly-...            # https://tavily.com/
OPENAI_API_KEY=sk-...              # https://platform.openai.com/
```

### 3. Run the app

```bash
streamlit run src/web_app/streamlit_app.py
```

Open `http://localhost:8501` in your browser.

---

## Usage Examples

### Research
```
"Research the latest trends in generative AI for 2025"
"What are the best practices for remote work productivity?"
```

### Blog Post
```
"Write a blog post about AI in healthcare"
"Create an SEO article about sustainable investing for millennials"
```

### LinkedIn Post
```
"Write a LinkedIn post about the importance of continuous learning"
"Create a professional update about launching a new SaaS product"
```

### Image Generation
```
"Generate an image for a fintech startup landing page"
"Create a professional header image about AI and creativity"
```

### Content Strategy
```
"Build a content strategy for a B2B SaaS company"
"Create a 4-week content calendar for a health and wellness brand"
```

---

## Project Structure

```
ContentAlchemy/
├── src/
│   ├── agents/           # 6 specialized agent implementations
│   ├── core/             # LangGraph workflow, router, config
│   ├── integrations/     # API clients (Anthropic, Tavily, OpenAI)
│   ├── utils/            # SEO scoring, quality validation
│   └── web_app/          # Streamlit UI + components
├── tests/
│   ├── unit/             # Unit tests with mocked API calls
│   └── integration/      # End-to-end tests (requires real API keys)
├── config/
│   └── settings.yaml     # Default configuration
├── requirements.txt
├── .env.example
└── README.md
```

---

## Running Tests

```bash
# Unit tests (no API keys needed — uses mocks)
pytest tests/unit/ -v

# Integration tests (requires real API keys in .env)
pytest tests/integration/ -v -m integration
```

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `ANTHROPIC_API_KEY not set` | Copy `.env.example` to `.env` and add your key |
| `TavilyClient error` | Check your `TAVILY_API_KEY` is valid |
| `OpenAI API error` | Check your `OPENAI_API_KEY` and billing |
| `Module not found` | Run `pip install -r requirements.txt` |
| `Streamlit won't start` | Run from the project root, not from inside `src/` |

---

## Cost Optimization Tips

- Claude Sonnet 4.6 is cost-efficient for production use
- Tavily's "advanced" search depth gives the best research quality
- DALL-E 3 standard quality costs less than HD — change in `config/settings.yaml`
- For high-volume use, add Redis caching for repeated topic searches

---

## Multi-Agent AI Project

A multi-agent content automation system built with LangGraph and Claude.

- Multi-agent orchestration with LangGraph
- 6 specialized agents with distinct capabilities
- Intelligent routing based on user intent
- Conversation memory across multi-turn interactions
- SEO scoring and quality validation pipeline
- Responsive Streamlit UI with content preview and analytics
