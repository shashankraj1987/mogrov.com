---
title: "DevTrack: Automated Ticket Management for Developers"
date: "Apr 2026"
category: devtrack
excerpt: "Introducing DevTrack — a local-first git daemon that eliminates manual ticket updates by learning how you commit and write."
readTime: 2
tags: buildinpublic,opensource,productivity
source: linkedin
sourceUrl: https://www.linkedin.com/feed/update/urn:li:activity:7440294239026159616/
---

Developers resist updating project management tickets after completing work. The process is tedious and disruptive — you've just shipped something, and now you have to context-switch to write about it in a tool you didn't open while writing it. DevTrack solves this by removing the manual step entirely.

## What It Does

- **Git-Based Automation:** Monitors commits and automatically syncs Azure DevOps, GitLab, and GitHub tickets.
- **Natural Language Planning:** Converts feature descriptions into Epics, Stories, and Tasks with automatic assignment.
- **Voice-Matched Updates:** Learns your communication style to write ticket updates that sound like you wrote them — not a generic AI.
- **Offline Capability:** Runs locally using Ollama and SQLite. Credentials stay on-device.
- **Mobile Control:** Full Telegram bot integration for managing tickets without opening a laptop.

## Where It's At

It's rough around the edges, open source, and in active development — but it gets the job done. The core loop (commit → ticket comment → standup update) works reliably. The rough edges are in configuration and the setup wizard, which I'm working through now.

If you're spending non-trivial time each day on ticket hygiene, give it a try. Local-first means your data doesn't leave your machine, and there's no per-seat pricing to argue about with finance.

[devtrack.cloud](https://devtrack.cloud) — source on [GitHub](https://github.com/sraj0501/automation_tools).
