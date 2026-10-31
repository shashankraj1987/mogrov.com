---
title: "Six Coding Harnesses, One Local Memory: DevTrack v3.2.0"
date: "Oct 21, 2026"
category: devtrack
excerpt: "DevTrack 3.2 adds Sage: a local command-knowledge system that turns useful activity from six coding harnesses into searchable Markdown without exposing raw sessions through MCP."
readTime: 6
tags: devtrack,opensource,localfirst,mcp
---

The frustrating part of using more than one coding assistant is not switching between them. It is watching each one forget what the last one learned.

A useful command gets worked out in Codex. A debugging pattern emerges in Claude Code. Cursor uncovers a repository-specific rule. A week later, the lesson is trapped in a transcript nobody will search again, or it has vanished with the session.

That is the problem behind **DevTrack v3.2.0**. This release adds DevTrack Sage, a local command-knowledge system that can observe useful development activity across six coding harnesses and turn it into durable, searchable Markdown.

It is a substantial release, but the goal is deliberately small: make the knowledge created while coding reusable without turning private development sessions into another cloud dataset.

## From disposable sessions to portable knowledge

Sage has independent adapters for:

- Codex
- Claude Code
- GitHub Copilot CLI
- OpenCode
- Cursor
- Devin

The adapters are additive and managed separately. You decide which environments participate. Captured activity moves through a bounded local queue and SQLite state before Sage publishes deterministic Markdown into a local knowledge base.

“Deterministic” matters here. The result is not a mysterious vector-store blob that only one application understands. It is readable text with stable structure: portable, diffable, searchable, and suitable for version control when you choose to track it.

Sage can search and list that knowledge, route entries to the right topic, merge related topics, repair its local indexes, and export or import Markdown. Retention and deletion are explicit operations. Destructive actions require confirmation, and opaque data that cannot be safely processed can be quarantined within bounded local storage.

The aim is useful memory with an exit door. You can inspect what was kept, move it, repair it, or remove it.

## MCP access without handing over the raw session

DevTrack's local MCP server now exposes ten read-only tools. Four of those tools let compatible assistants search Sage knowledge, list topics, retrieve a published entry, and inspect bounded pipeline status.

The boundary is as important as the feature. MCP receives published knowledge and limited diagnostics. It does **not** expose raw Sage events, prompts, model output, reasoning, logs, or adapter configuration paths.

That separation gives an assistant enough context to answer “How do we do this in this repository?” without giving it a pipe into every captured interaction that produced the answer.

The MCP server remains local stdio, and the Sage path is Go-native. Python is not required to capture, publish, search, or serve this knowledge. Ollama remains the offline-first model path, while external providers are available only when explicitly configured.

## The less visible fixes may matter more each day

Sage is the headline, but v3.2.0 also closes several pieces of daily workflow friction.

Ticket mapping is now deterministic. Branches resolve to work items using explicit workspace rules, stored provenance, and an immutable correction audit. When the automatic choice is wrong, a correction does not silently erase the history of how it happened.

DevTrack can also infer bounded work sessions from local activity while preserving explicit corrections. This is intentionally silent: it should improve the raw material for a standup update without becoming another timer demanding attention.

The Git path received a necessary correction too. Normal Git commands no longer pass through the interactive enhanced-commit flow. Generated observation hooks stay silent and fail open, while an explicitly requested enhanced commit returns as soon as Git succeeds. A tool that watches Git should not make Git feel less reliable.

Finally, upgrades can follow either the stable channel or the rolling development channel:

```sh
devtrack upgrade --main
devtrack upgrade --dev
```

That makes the choice explicit for people who want released behavior and for contributors who want to test the newest integrated build.

## Packaged for the places developers actually work

The release publishes native binaries for Windows amd64, Linux amd64 and arm64, and macOS amd64 and arm64. The same five platforms have native MCPB bundles, and the release includes checksums plus validated MCP registry metadata.

DevTrack is also published in the official MCP Registry as `io.github.sraj0501/devtrack`. In total, the v3.2.0 GitHub release contains 12 assets, and the release workflow smoke-tested all five native MCPB packages.

Existing v3.1.x configuration and SQLite data remain supported.

## What is still rough

This release does not pretend every part of DevTrack is equally complete.

The optional managed Python features still require PostgreSQL and an explicitly configured service. Several communication-learning HTTP adapters remain incomplete, so Teams and Outlook learning should not be treated as available yet. The server-admin visual redesign was deliberately left out of v3.2.0 because it needs a separate drift and UI-acceptance pass.

Those boundaries are documented because “local-first” should describe the actual data path, not decorate the landing page. The Go client, standup workflow, Sage knowledge path, local MCP server, SQLite storage, and Ollama integration can work offline. Hosted models and managed services are choices, not hidden requirements.

## Try the release

Start with the [DevTrack documentation](/wiki/devtrack/), then follow the [quick start](/wiki/devtrack/#QUICK_START). The [Sage guide](/wiki/devtrack/#SAGE) covers local command knowledge, and the [MCP guide](/wiki/devtrack/#MCP_CLAUDE_CODE) explains how to connect a compatible assistant.

The complete binaries, checksums, MCPB bundles, and technical release notes are on the v3.2.0 GitHub release.

DevTrack still starts from the same promise: write the standup update from the work you already did. v3.2.0 adds a second promise beside it: the useful things your tools learn while you work should still be there tomorrow.
