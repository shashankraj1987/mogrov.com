# pm-config.md
# Global agent configuration for mogrov.com.
# Agents read this file at startup (Step 0) to understand project context.
# Schema reference: ~/.claude/AGENT_AUTHORING.md

```yaml
project:
  name: mogrov.com
  description: "Marketing / landing site for Mogrov, a developer-first tools collective (single-file static site)."
  languages: [HTML, JavaScript, CSS]
  type: web   # static single-page marketing site

paths:
  src: [./]              # single-file project — index.html lives at root
  board: .claude/project_board.md
  engineer_log: .claude/engineer_log.md
  feature_tracker: .claude/feature_tracker.md
  posts_dir: .claude/posts/
  memory_project: .claude/memory/
  memory_user: C:\Users\sraj\.claude\projects\D--git-apps-mogrov-com\memory   # confirmed to exist on disk

git:
  default_branch: master      # repo initialized on 'master'; no commits/remote yet
  merge_target: master        # No integration branch found — create a 'dev' branch or update this field
  branch_prefixes: [feature/, fix/, docs/]   # default convention — no branch history yet to detect from
  push_prefix: "GIT_NO_DEVTRACK=1"           # devtrack git hooks present — set to skip on routine pushes

commit:
  tool: devtrack              # devtrack.exe found in PATH
  command: devtrack git commit
  fallback: git commit

test:
  commands: []                # No test framework — static site. Add test/lint commands here if a toolchain is introduced.

scan:
  paths: [./]
  file_types: ["*.html", "*.js", "*.css"]
  exclude: []

vision:
  rules:
    # Add project-specific non-negotiables. Examples:
    # - "single-file: keep everything in index.html unless a build step is deliberately introduced"
    # - "offline-first / OSS: align messaging with the stated brand values"
    # - "CDN-only deps: no local package install without explicit decision"
  pm_system: none   # github | jira | azure | linear | none

posts:
  author: ""        # Fill in: your name for post attribution
  platform: dev.to  # dev.to | hashnode | medium | substack
```
