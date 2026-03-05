# CLAUDE.md

> Purpose: This repository is a content hub and static website for AI
> news and content ideas (LLM → Agentic → Multi‑Agent → AGI → ASI).
> Claude Code is used as an autonomous content agent to update markdown
> files in docs/ and propose changes via branch + pull request.

------------------------------------------------------------------------

## Repository Goals

1.  Maintain a daily-updated archive of AI news with sources.
2.  Convert news into content ideas for TikTok, YouTube, Instagram and
    blog posts.
3.  Publish everything as a static site.

Claude must optimize for accuracy, structure and consistency over hype.

------------------------------------------------------------------------

## Folder Structure

Claude must write content only into these directories:

docs/ index.md news/ YYYY-MM/ daily-YYYY-MM-DD.md week-XX.md ideas/
YYYY-MM/ daily-YYYY-MM-DD.md week-XX.md sources/ trusted_sources.md
news_feeds.md

templates/ news-brief.md content-ideas.md

Rules:

-   Never rename these folders
-   Create missing folders if needed
-   Do not edit workflow files unless explicitly instructed

------------------------------------------------------------------------

## AI Capability Stages

Each news item and content idea must include at least one of these tags:

llm -- LLM models, prompting, RAG, embeddings, fine tuning\
agentic -- AI agents, tool use, automation workflows\
multi-agent -- agent collaboration systems\
agi -- artificial general intelligence discussions\
asi -- superintelligence or existential risk discussions

Optional tags:

policy, safety, security, research, hardware, startups, education

------------------------------------------------------------------------

## News File Format

Path:

docs/news/YYYY-MM/daily-YYYY-MM-DD.md

Structure example:

# Daily AI News --- YYYY-MM-DD

## Headline

What happened: short explanation

Why it matters: explanation for creators

Sources: - link - link

Tags: llm, agentic

Rules:

-   10--20 items per day
-   every item must have sources
-   skip items without sources
-   avoid duplicates

------------------------------------------------------------------------

## Content Idea Format

Path:

docs/ideas/YYYY-MM/daily-YYYY-MM-DD.md

Example:

# Daily Content Ideas --- YYYY-MM-DD

## Idea: Why AI Agents Will Change Software

Hook: "Everyone talks about ChatGPT, but the real revolution is AI
agents."

Core points: - LLMs generate text - agents execute actions - automation
of workflows

Format: TikTok / Reel / YouTube

CTA: Follow for more AI explanations

Tags: agentic

Rules:

-   20--40 ideas per day
-   avoid repeated hooks
-   keep ideas educational

------------------------------------------------------------------------

## Writing Style

Language: German

Tone: - educational - simple explanations - technically correct

Avoid hype or exaggerated claims.

------------------------------------------------------------------------

## Source Policy

Allowed sources:

-   official company announcements
-   research papers
-   reputable tech publications

Examples:

OpenAI\
Anthropic\
Google DeepMind\
MIT Technology Review\
Wired\
Nature\
Science

Claude must never invent sources.

------------------------------------------------------------------------

## Operational Rules

Preferred workflow:

-   create branch content/daily-YYYY-MM-DD
-   commit changes
-   open pull request

Commit examples:

Daily news update: YYYY-MM-DD\
Daily content ideas: YYYY-MM-DD

Claude must not:

-   push directly to main
-   modify workflows
-   delete large parts of the repository

------------------------------------------------------------------------

## Daily Automation

When executed automatically:

1.  Create news file for today's date
2.  Create ideas file for today's date
3.  Update docs/index.md with newest links
4.  ensure formatting is correct
