---
title: "I Turned My Google Sheets Hack Into a Real Tool. It Took Six Months and I Have No Regrets."
date: "Apr 5, 2025"
category: product
excerpt: "From spreadsheet + cron job to a 5 MB Go daemon with 94% automatic ticket updates. The architecture and the numbers."
readTime: 6
tags: devtrack,golang,startup
source: devto
sourceUrl: https://dev.to/shashank_raj/i-turned-my-google-sheets-hack-into-a-real-tool-it-took-six-months-and-i-have-no-regrets-5cj3
---

A while back I wrote about automating standups using Google Sheets, a cron job, and makeshift infrastructure. It worked — until a PM asked for ticket updates to happen *before* standups rather than after. The system collapsed. That failure prompted a complete rewrite.

## The Problem with the Old Approach

The original Google Sheet approach still required manual work each night in a specific format. Silent failures occurred when formatting was incorrect. What I wanted was true automation: *commit code, ticket updates itself, standup writes itself, I do nothing.*

Existing tools either required SaaS vendors, charged per-seat fees, or didn't support local-first workflows with personal LLMs. So I built my own.

## How DevTrack Works

DevTrack is a Go daemon that monitors git repositories. It processes commits and timer triggers (configurable, every ~90 minutes by default), routing data to a Python backend running NLP and LLM operations. Updates then push to PM tools — Azure DevOps, GitHub, or Jira.

The flow from a single commit:

1. Commit message receives AI enrichment
2. NLP extracts context and cross-references open items
3. Comments post to relevant tickets
4. Tickets auto-advance based on branch patterns
5. Standup content auto-populates

Processing time: approximately 4 seconds from commit to ticket comment.

## Six Months of Numbers

- ~23 minutes saved daily on ticket updates and standup prep
- 94% automatic work item updates
- Pre-written standups 4 out of 5 days per week
- Zero manual 11pm Jira sessions since January

## What Ships with v1.0

**Daily use:** Git commit interception, PM tool sync (Azure DevOps, GitHub, Jira), ticket alerts, EOD report generation, and *git-sage* — an agentic tool for rebases and conflict resolution.

**Less frequent features:** GitLab integration, Telegram bot, Teams communication analysis.

The binary is 5 MB. Local LLM support via Ollama means it runs fully offline. Multi-platform: macOS and Linux (arm64/amd64). No account required for local usage.

## The Voice Personalization Pipeline

A month-long pipeline analyses your communication patterns — short sentences, specific phrasing, your vocabulary — and generates updates that sound like you wrote them, not a generic AI. This was the hardest part to get right and the part people notice first.

## What's Next

A local-first admin console is on the roadmap. I'm also planning to experiment with handing an AI agent all my commits for two months and seeing what it learns about how I work.

If you spend 15+ minutes daily on ticket updates or standup notes, [DevTrack](https://devtrack.cloud) is worth trying. Data stays on your machine. No accounts, no API keys required for the Ollama path.
