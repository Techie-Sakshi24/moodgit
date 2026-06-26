"""
MoodGit - Emotional timeline of your git commits
"""

import os
import json
from datetime import datetime
from typing import Optional
import anthropic
from git import Repo, InvalidGitRepositoryError


EMOTION_SYSTEM_PROMPT = """You are MoodGit, a witty but accurate emotion analyst for git commit messages.

Given a list of git commit messages with timestamps, analyze the emotional state of the developer.

Respond ONLY with a valid JSON array (no markdown, no backticks, no explanation). Each item:
{
  "hash": "short hash",
  "message": "original message",
  "emotion": "one of: focused | stressed | excited | tired | frustrated | celebratory | confused | determined | casual",
  "intensity": 1-10,
  "vibe": "one witty sentence (max 12 words) about this commit's energy",
  "timestamp": "original timestamp"
}

Rules:
- ALL CAPS = stressed or excited
- typos, no punctuation = tired
- "fix", "bug", "broken", "revert" = frustrated or stressed
- "feat", "add", "implement" = focused or excited
- "wip", "temp", "todo" = confused or casual
- "final", "done", "release", "v1" = celebratory
- Very short messages like "." or "asdf" = tired (3am energy)
- Profanity = frustrated (be understanding, not judgmental)
- Time of commit matters: 12am-4am = probably tired or stressed"""


def get_commits(repo_path: str, limit: int = 50, branch: Optional[str] = None):
    """Extract commits from a git repo."""
    try:
        repo = Repo(repo_path)
    except InvalidGitRepositoryError:
        raise ValueError(f"'{repo_path}' is not a valid git repository.")

    active_branch = branch or repo.active_branch.name
    commits = []

    for commit in list(repo.iter_commits(active_branch))[:limit]:
        dt = datetime.fromtimestamp(commit.committed_date)
        commits.append({
            "hash": commit.hexsha[:7],
            "message": commit.message.strip().split("\n")[0],  # first line only
            "timestamp": dt.strftime("%Y-%m-%d %H:%M"),
            "hour": dt.hour,
            "author": commit.author.name,
        })

    return commits, repo


def analyze_emotions(commits: list, api_key: Optional[str] = None) -> list:
    """Send commits to Claude for emotion analysis."""
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError("ANTHROPIC_API_KEY not set. Export it or pass --api-key.")

    client = anthropic.Anthropic(api_key=key)

    # Send in batches of 20 to avoid token limits
    results = []
    batch_size = 20

    for i in range(0, len(commits), batch_size):
        batch = commits[i:i + batch_size]
        commit_text = json.dumps(batch, indent=2)

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            system=EMOTION_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze these commits:\n{commit_text}"
                }
            ]
        )

        raw = response.content[0].text.strip()

        # Strip any accidental markdown fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        batch_results = json.loads(raw)
        results.extend(batch_results)

    return results


def compute_summary(analyzed: list) -> dict:
    """Compute stats across all analyzed commits."""
    emotion_counts = {}
    total_intensity = 0
    late_night_count = 0
    most_stressed = None
    most_excited = None
    highest_intensity = 0

    for c in analyzed:
        emotion = c.get("emotion", "unknown")
        intensity = c.get("intensity", 5)
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        total_intensity += intensity

        hour_str = c.get("timestamp", "")
        # Check late night commits
        try:
            hour = int(hour_str.split(" ")[1].split(":")[0])
            if hour >= 23 or hour <= 4:
                late_night_count += 1
        except Exception:
            pass

        if intensity > highest_intensity:
            highest_intensity = intensity
            if emotion in ("stressed", "frustrated"):
                most_stressed = c
            elif emotion in ("excited", "celebratory"):
                most_excited = c

    dominant_emotion = max(emotion_counts, key=emotion_counts.get) if emotion_counts else "unknown"
    avg_intensity = round(total_intensity / len(analyzed), 1) if analyzed else 0

    return {
        "dominant_emotion": dominant_emotion,
        "emotion_counts": emotion_counts,
        "avg_intensity": avg_intensity,
        "late_night_commits": late_night_count,
        "most_stressed_commit": most_stressed,
        "most_excited_commit": most_excited,
        "total_commits": len(analyzed),
    }
