---
title: "Your Logs Should Read Like a Status Report, and Your Errors Should Arrive Pre-Diagnosed"
date: "Jul 5, 2026"
category: engineering
excerpt: "runtime-narrative 1.5 turns execution into a readable story: emoji-clean logs on success, a full diagnosis — and an LLM-suggested fix — on failure."
readTime: 4
tags: python,opensource,observability
source: linkedin-discussion
---

You know the moment. Something failed in production, and what you have to work with is a 40-frame stack trace and a wall of log lines that were written for the machine, not for you. You spend the next hour playing archaeologist: what ran? what succeeded? what state was it in when it died?

runtime-narrative exists to delete that hour. It turns your program's execution into a story you can read. Here's real output from a CSV import that dies on a duplicate key:

```term
22:18:45.003 [221892] ▶ Story started: Import Customers
  22:18:45.098 [221892] INFO [Load CSV] shop.orders: parsed 8412 rows from customers.csv
  22:18:45.099 [221892] ✔ Stage completed: Load CSV (0.096s)
  22:18:45.239 [221892] ✔ Stage completed: Validate Data (0.141s)
  22:18:45.240 [221892] ▶ Stage started: Insert Records

  22:18:45.242 [221892] ❌ Failure detected
Story: Import Customers
Stage: Insert Records
Error: ValueError - duplicate key 'cust_4820' violates unique constraint on customers
Location: importer.py:53 (insert_rows)
Context:
      51 |     inserted = 4820
      52 |     duplicate = rows[4820]["id"]
  >   53 |     raise ValueError(f"duplicate key '{duplicate}' violates unique constraint on {table}")
Locals (rich diagnostics):
    batch_size = 500
    duplicate = 'cust_4820'
    inserted = 4820
    rows = [{'id': 'cust_0001'}, {'id': 'cust_0002'}, {'id': 'cust_0003'}, ...]
Stage timeline: Load CSV=completed (0.096s) | Validate Data=completed (0.141s) | Insert Records=failed
Progress: 66% (2 / 3)
22:18:45.243 [221892] ▶ Story ended: FAILED (0.240s)
```

Read what you just got, for free: which stages succeeded and how long each took, the exact line that raised, the source around it, and the local variable values at the moment of death — `duplicate = 'cust_4820'`, 4,820 rows in. Secrets are redacted automatically. On success you only see the ✔ lines: clean, glanceable, done. No reconstruction. The error report *is* the investigation.

And if you point it at an LLM — Ollama running locally, any OpenAI-compatible endpoint, or Claude — it goes one step further: the failure arrives with a suggested fix, naming the exact location, before you've even opened your editor. It runs in the background, never blocks your app, and shuts up if the endpoint is down.

That's the pitch. It's been the pitch since 0.2. What 1.5 changes — twelve releases in five weeks — is the ceiling on where you can use it.

## Sub-story tracing

This is the headline. In 0.2, a story was flat: one workflow, a list of stages. Real systems don't work like that. An API request kicks off a DB query, which triggers a cache rebuild, which calls another service. Before, each of those was its own disconnected story — when the cache rebuild failed, you couldn't see the request that caused it.

Now nested stories link automatically:

```python
from runtime_narrative import story, stage

with story("Process order #10452"):
    with stage("Charge card"):
        charge(cart)  # internally opens story("Payment provider call")
```

And this is what that renders — the payment sub-story gets its own id (`48c4b7`) and nests under the stage that spawned it:

```term
22:18:44.579 [379e3c] ▶ Story started: Process order #10452
  22:18:44.629 [379e3c] INFO [Load cart] shop.orders: 3 items, total $184.50
  22:18:44.630 [379e3c] ✔ Stage completed: Load cart (0.051s)
  22:18:44.730 [379e3c] WARNING [Reserve inventory] shop.orders: SKU 'MUG-BLUE' low stock: 2 left
  22:18:44.731 [379e3c] ✔ Stage completed: Reserve inventory (0.101s)
  22:18:44.731 [379e3c] ▶ Stage started: Charge card
    22:18:44.731 [48c4b7] ▶ Story started: Payment provider call
      22:18:44.851 [48c4b7] INFO [Authorize] shop.orders: authorized $184.50 on card ending 4821
      22:18:44.852 [48c4b7] ✔ Stage completed: Authorize (0.121s)
      22:18:44.932 [48c4b7] ✔ Stage completed: Capture (0.080s)
    22:18:44.932 [48c4b7] ▶ Story ended: SUCCESS (0.201s)
  22:18:44.932 [379e3c] ✔ Stage completed: Charge card (0.202s)
  22:18:45.002 [379e3c] ✔ Stage completed: Send confirmation (0.070s)
22:18:45.003 [379e3c] ▶ Story ended: SUCCESS (0.424s)
```

If the payment story fails three layers down, the failure report shows the full chain: which request, which stage, which sub-story — every step that succeeded before things went wrong. That was always the promise for one story. Now it holds across the whole call graph.

## It meets your code where it is

The honest criticism of 0.2 was adoption cost: `with` blocks everywhere. Two answers in 1.5:

- **Auto-instrumentation** — point it at a module or class and every method becomes a stage. Zero call-site changes.
- **Logging bridge** — your existing `logging` calls get captured and routed into the active story. Those `INFO` and `WARNING` lines in the trace above? Plain stdlib `logger.info(...)` calls — one handler attached, and every log line you've written over the years lands inside the stage that emitted it, instead of in a second, disconnected stream. (The console renderer takes a `level_icons` map too, if you want 💬/⚠️/🔥 instead of level names in your terminal.)

You can now try runtime-narrative on a codebase you're afraid to touch, which is exactly the kind of codebase that needs it.

## From terminal tool to observability citizen

0.2 rendered to the console and JSON. That's a dev tool. 1.5 adds SQLite, HTML reports, webhooks — and OpenTelemetry and Prometheus renderers, so stories show up in the tracing and metrics stack you already run instead of competing with it. Framework middleware grew from FastAPI-only to Django, Celery, and gRPC.

Everything ships as optional extras (`pip install runtime-narrative[otel]`), so the core stays lean.

## LLM analysis, now with Claude

The fix-suggestion engine from the intro gained native Anthropic Claude support in 1.5, alongside the existing Ollama and OpenAI-compatible options. Worth repeating: the library is fully useful with no LLM at all — the analysis is a bonus, not a dependency.

## The short version

0.2 was a good idea with a small blast radius. 1.5 is the same idea, production-shaped: it follows requests across boundaries, installs into code you didn't write, and reports into the systems you already watch.

```bash
pip install runtime-narrative
```

It's on PyPI, MIT-licensed, Python 3.9+. If you try it on a real codebase, I want to hear what broke — that's how the last twelve releases happened.
