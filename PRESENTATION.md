---
marp: true
theme: default
paginate: true
style: |
  section {
    font-family: 'Segoe UI', sans-serif;
  }
  section.title {
    text-align: center;
    background: #0f172a;
    color: #f8fafc;
  }
  section.title h1 { font-size: 2.4em; color: #38bdf8; }
  section.title h2 { font-size: 1.2em; color: #94a3b8; font-weight: normal; }
  h1 { color: #0f172a; border-bottom: 3px solid #38bdf8; padding-bottom: 8px; }
  code { background: #f1f5f9; padding: 2px 6px; border-radius: 4px; }
  table { width: 100%; }
  th { background: #0f172a; color: #f8fafc; }
---

<!-- _class: title -->

# ContentAlchemy
## AI Content Marketing Assistant

Multi-agent LangGraph system with Claude Sonnet 4.6

**Multi-Agent AI Project**
UpskillStudio

---

# The Problem

Content marketing teams face a constant challenge:

- Research takes hours across dozens of sources
- Writing SEO-optimized blog posts requires specialized skill
- LinkedIn posts need a completely different voice and format
- Consistent content strategy is hard to maintain at scale
- Image brief creation is a separate workflow entirely

**ContentAlchemy solves all of this in one conversational interface.**

---

# Solution Overview

A **multi-agent AI system** that routes user intent to the right specialist agent — automatically.

```
User types one request → System routes → Right agent responds
```

| User says... | Agent activated |
|---|---|
| "Research generative AI trends" | Research Agent |
| "Write a blog post about AI in healthcare" | Research → Blog Writer |
| "Create a LinkedIn post about leadership" | LinkedIn Writer |
| "Generate a landing page image for fintech" | Image Generator |
| "Build a 4-week content calendar for SaaS" | Research → Content Strategist |

---

# Architecture

```
User Input
    │
    ▼
┌─────────────────┐
│  Query Handler  │  ← Claude extracts intent, topic, audience, tone
└────────┬────────┘
         │ conditional routing (LangGraph)
    ┌────┴──────────────────────────────────┐
    │                                       │
    ▼                                       ▼
┌──────────────┐                   ┌─────────────────────┐
│ Research     │                   │  LinkedIn Writer    │
│ Agent        │                   │  Image Generator    │
│ (Tavily +    ├──────────────────►│  Content Strategist │
│  Claude)     │  blog / strategy  └─────────────────────┘
└──────┬───────┘
       │ blog route
       ▼
┌──────────────┐
│  Blog Writer │  ← SEO-optimized with research context
└──────────────┘
```

---

# The 6 Agents

| Agent | Capability |
|---|---|
| **Query Handler** | Parses user intent with Claude, routes to correct agent |
| **Research Agent** | Tavily web search + Claude synthesis into structured report |
| **Blog Writer** | 800–1500 word SEO blog with quality + SEO scoring |
| **LinkedIn Writer** | Engagement-optimized post with hashtag strategy |
| **Image Generator** | Claude-optimized prompt → DALL-E 3 image |
| **Content Strategist** | 4-week content strategy brief from research data |

Each agent is a **standalone, testable function** that reads and writes to shared LangGraph state.

---

# Tech Stack

| Layer | Technology | Why |
|---|---|---|
| LLM | Claude Sonnet 4.6 | Best-in-class reasoning, instruction following |
| Orchestration | LangGraph + MemorySaver | Stateful multi-agent graph with memory |
| Research | Tavily AI | Real-time web search with structured results |
| Image | DALL-E 3 | High-quality image generation |
| Config | Pydantic Settings | Type-safe settings + `.env` loading |
| UI | Streamlit | Fast interactive web app |
| Tests | pytest + mocks | 25 unit tests, no API calls needed |

---

# LangGraph Workflow

Two routing decisions drive the entire system:

**After Query Handler:**
- `research` → Research Agent → END
- `blog` → Research Agent → Blog Writer → END
- `linkedin` → LinkedIn Writer → END
- `image` → Image Generator → END
- `strategy` → Research Agent → Content Strategist → END

**Key design decision:** Blog and Strategy routes run Research *first*, so the writer always has current, factual data to work with.

**Conversation memory** is preserved across turns via `MemorySaver`.

---

# SEO & Quality Pipeline

Every piece of content passes through two validators before returning:

**SEO Scoring** (`content_optimization.py`)
- Keyword extraction (TF-IDF style, stop-word filtered)
- Heading structure analysis (H1/H2 presence)
- Meta description generation (≤160 chars)
- Overall SEO score (0–100)

**Quality Validation** (`quality_validation.py`)
- Word count vs. content-type minimums
- Structure checks (headings, hashtags)
- Readability (long sentence detection)
- Pass/fail threshold at 60/100

---

# Testing

**25 unit tests — all passing — zero API calls required**

```
tests/unit/
├── test_agents.py      # QueryHandler, Research, LinkedIn, Blog
└── test_workflow.py    # Router logic, SEO scoring, quality validation
```

Key testing patterns used:
- `unittest.mock.patch` — mock at the point of use (not the source module)
- All external APIs mocked: Anthropic, Tavily, OpenAI
- Edge cases covered: empty input, invalid JSON, API failures, short content

```bash
pytest tests/unit/ -v   # Runs in < 1 second, no keys needed
```

---

# Live Demo

**Try these prompts in the app:**

1. `Research the latest trends in agentic AI for 2025`
   → Tavily search + Claude synthesis report

2. `Write a blog post about AI in healthcare for hospital administrators`
   → Research + SEO-optimized 1000+ word blog

3. `Create a LinkedIn post about the importance of continuous learning`
   → Engagement-optimized post with hashtags

4. `Build a content strategy for a B2B SaaS startup in HR tech`
   → Full 4-week content calendar with themes, KPIs, channels

---

# Key Engineering Decisions

**Why LangGraph over a simple chain?**
Stateful graph enables branching, multi-step flows, and memory — not possible with a linear chain.

**Why separate agents instead of one big prompt?**
Each agent has a focused system prompt. Specialization produces dramatically better output quality.

**Why Tavily before writing?**
Blog posts and strategies grounded in real current data are more credible and factually accurate.

**Why Claude for prompt optimization (image agent)?**
DALL-E 3 responds best to highly structured prompts. Claude produces better prompts than raw user input.

---

# What I Built & Learned

**Built:**
- Full multi-agent system with 6 specialized agents
- Intelligent routing based on natural language intent
- SEO scoring + quality validation pipeline
- Streamlit chat UI with content preview
- 25-test unit suite with proper mock isolation

**Learned:**
- LangGraph state management and conditional edges
- Python circular import patterns and how to avoid them
- Mock patching strategy: patch where the name is *used*, not where it's defined
- Agentic system design: when to use one agent vs. many

---

<!-- _class: title -->

# Thank You

**ContentAlchemy** — AI Content Marketing Assistant

```bash
streamlit run src/web_app/streamlit_app.py
```

`http://localhost:8501`

---
Stack: Claude Sonnet 4.6 · LangGraph · Tavily · DALL-E 3 · Streamlit
