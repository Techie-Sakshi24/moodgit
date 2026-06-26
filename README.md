# 📊 MoodGit

> **Your commits have feelings. Now you can see them.**

MoodGit analyzes the emotional tone of your git commit history using Claude AI and renders a timeline showing stress peaks, hype moments, late-night grind sessions, and your overall project vibe.

![Python](https://img.shields.io/badge/Python-3.8%2B-3776ab?logo=python&logoColor=white)
![Claude AI](https://img.shields.io/badge/Powered%20by-Claude%20AI-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Stars](https://img.shields.io/github/stars/Techie-Sakshi24/moodgit?style=social)


## What it does

```
📊 MoodGit — your commits have feelings
─────────────────────────────────────────────────────────────────────

 Hash     Timestamp          Emotion          Intensity   Message
 ───────  ─────────────────  ───────────────  ──────────  ─────────────────────────
 a3f92c1  2024-01-15 02:47   😴 tired         ██████░░░░  fix
 b7e1d44  2024-01-15 03:12   😤 stressed      █████████░  WHYYY IS THIS NOT WORKING
 c8a2b33  2024-01-15 09:30   🎯 focused       ███████░░░  refactor auth middleware
 d4f9e11  2024-01-16 14:22   🚀 excited       ██████████  feat: OAuth finally works!!
 e2c7a98  2024-01-16 15:01   🎉 celebratory   █████████░  v1.0.0 — ship it

📊 MoodGit Summary
╭──────────────────────────────────────────────────────────╮
│  Repo: my-project    Commits: 5    Avg intensity: 8.2/10 │
│  Dominant vibe: 😤 stressed                              │
│                                                           │
│  Emotion breakdown:                                       │
│    😤 stressed      ████████  3                           │
│    🚀 excited       ████░░░░  1                           │
│    🎉 celebratory   ████░░░░  1                           │
│                                                           │
│  Late nights: 2 late-night commits (11pm–4am)            │
│  💀 Peak stress: b7e1d44 — WHYYY IS THIS NOT WORKING     │
│  🏆 Hype moment: d4f9e11 — feat: OAuth finally works!!   │
╰──────────────────────────────────────────────────────────╯
```

It also generates a **beautiful HTML report** with a doughnut chart and dark-mode timeline you can share.


## Install

```bash
pip install moodgit
```

Or clone and install locally:

```bash
git clone https://github.com/Techie-Sakshi24/moodgit.git
cd moodgit
pip install -e .
```

## Setup

You need an Anthropic API key. Get one free at [console.anthropic.com](https://console.anthropic.com).

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Or add it to your `.bashrc` / `.zshrc` to make it permanent.

## Usage

```bash
# Analyze current repo, last 30 commits
moodgit

# Analyze a different repo
moodgit /path/to/your/repo

# Analyze more commits
moodgit -n 100

# Analyze a specific branch
moodgit --branch main

# Export an HTML report
moodgit --html report.html

# Skip the per-commit table (just show summary)
moodgit --no-table

# All options
moodgit /path/to/repo -n 50 --branch dev --html my-report.html
```

## Emotions detected

| Emotion | Trigger patterns |
|---|---|
| 🎯 focused | `feat`, `implement`, `add`, `refactor` |
| 😤 stressed | ALL CAPS, `broken`, `HELP`, `why` |
| 🚀 excited | `!!`, `finally`, `works`, `amazing` |
| 😴 tired | typos, single chars (`.`, `x`), 2–4am commits |
| 😤 frustrated | `bug`, `fix`, `revert`, `again`, profanity |
| 🎉 celebratory | `v1`, `release`, `done`, `deploy`, `ship` |
| 🤔 confused | `wip`, `temp`, `idk`, `todo`, `??` |
| 💪 determined | `keep going`, `almost`, `nearly` |
| 😎 casual | short vague messages with no urgency |

## HTML Report

Run with `--html report.html` to get a shareable dark-mode report:

- Doughnut chart of emotion breakdown
- Full commit timeline with color-coded badges
- Peak stress and hype moment callouts
- Late-night commit count

---

## Requirements

- Python 3.8+
- An Anthropic API key (Claude Sonnet)
- A git repo with at least a few commits (obviously)

---

## How it works

1. Uses **GitPython** to extract commit messages + timestamps from your repo
2. Sends them in batches to **Claude Sonnet** with a carefully crafted system prompt
3. Claude returns structured JSON with emotion labels, intensity scores, and a witty one-liner per commit
4. **Rich** renders the terminal UI; a custom HTML generator builds the report

## Contributing

PRs welcome. Ideas for future features:

- [ ] GitHub Actions integration (auto-generate report on push)
- [ ] Team mood aggregation across contributors
- [ ] Weekly/monthly trend charts
- [ ] Slack/Discord bot that posts your repo's weekly vibe
- [ ] `.moodgitignore` to exclude merge commits

## License

MIT — use it, fork it, build on it.

Made by [Sakshi Kale](https://github.com/Techie-Sakshi24) · Powered by [Claude AI](https://anthropic.com)
