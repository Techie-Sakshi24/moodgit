"""
MoodGit - HTML report generator
"""

import json
from datetime import datetime

EMOTION_COLORS = {
    "focused":      "#00bcd4",
    "stressed":     "#f44336",
    "excited":      "#ffc107",
    "tired":        "#607d8b",
    "frustrated":   "#9c27b0",
    "celebratory":  "#4caf50",
    "confused":     "#ff9800",
    "determined":   "#2196f3",
    "casual":       "#9e9e9e",
    "unknown":      "#444444",
}

EMOTION_EMOJI = {
    "focused":      "🎯",
    "stressed":     "😤",
    "excited":      "🚀",
    "tired":        "😴",
    "frustrated":   "😤",
    "celebratory":  "🎉",
    "confused":     "🤔",
    "determined":   "💪",
    "casual":       "😎",
    "unknown":      "❓",
}


def generate_html(analyzed: list, summary: dict, repo_name: str) -> str:
    commits_json = json.dumps(analyzed)
    counts = summary["emotion_counts"]
    chart_labels = json.dumps(list(counts.keys()))
    chart_data = json.dumps(list(counts.values()))
    chart_colors = json.dumps([EMOTION_COLORS.get(e, "#888") for e in counts.keys()])

    commit_rows = ""
    for c in analyzed:
        emotion = c.get("emotion", "unknown")
        color = EMOTION_COLORS.get(emotion, "#888")
        emoji = EMOTION_EMOJI.get(emotion, "❓")
        intensity = c.get("intensity", 5)
        bar_width = intensity * 10

        commit_rows += f"""
        <tr>
          <td><code>{c.get("hash","?")}</code></td>
          <td class="ts">{c.get("timestamp","")}</td>
          <td><span class="badge" style="background:{color}">{emoji} {emotion}</span></td>
          <td>
            <div class="bar-wrap">
              <div class="bar" style="width:{bar_width}%;background:{color}"></div>
            </div>
            <span class="int-num">{intensity}/10</span>
          </td>
          <td class="msg">{c.get("message","")[:60]}</td>
          <td class="vibe">{c.get("vibe","")}</td>
        </tr>"""

    dominant = summary["dominant_emotion"]
    dom_emoji = EMOTION_EMOJI.get(dominant, "❓")
    dom_color = EMOTION_COLORS.get(dominant, "#888")
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MoodGit Report — {repo_name}</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: #0d1117;
      color: #c9d1d9;
      min-height: 100vh;
      padding: 2rem;
    }}
    .header {{
      text-align: center;
      padding: 2rem 0 3rem;
    }}
    .header h1 {{
      font-size: 2.5rem;
      font-weight: 800;
      background: linear-gradient(135deg, #58a6ff, #bc8cff);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 0.5rem;
    }}
    .header p {{ color: #8b949e; font-size: 1rem; }}
    .cards {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 1rem;
      margin-bottom: 2rem;
    }}
    .card {{
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 12px;
      padding: 1.5rem;
      text-align: center;
    }}
    .card .val {{
      font-size: 2rem;
      font-weight: 700;
      margin-bottom: 0.3rem;
    }}
    .card .label {{ color: #8b949e; font-size: 0.85rem; }}
    .chart-wrap {{
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 12px;
      padding: 1.5rem;
      margin-bottom: 2rem;
      max-width: 500px;
    }}
    .chart-wrap h2 {{ margin-bottom: 1rem; font-size: 1rem; color: #8b949e; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 12px;
      overflow: hidden;
      font-size: 0.875rem;
    }}
    th {{
      background: #1c2128;
      color: #8b949e;
      font-weight: 600;
      padding: 0.75rem 1rem;
      text-align: left;
      border-bottom: 1px solid #30363d;
    }}
    td {{
      padding: 0.7rem 1rem;
      border-bottom: 1px solid #21262d;
      vertical-align: middle;
    }}
    tr:last-child td {{ border-bottom: none; }}
    tr:hover td {{ background: #1c2128; }}
    .badge {{
      display: inline-block;
      padding: 0.25rem 0.6rem;
      border-radius: 999px;
      font-size: 0.75rem;
      font-weight: 600;
      color: #fff;
    }}
    .bar-wrap {{
      background: #21262d;
      border-radius: 4px;
      height: 6px;
      width: 80px;
      display: inline-block;
      vertical-align: middle;
      margin-right: 6px;
    }}
    .bar {{ height: 100%; border-radius: 4px; }}
    .int-num {{ font-size: 0.75rem; color: #8b949e; }}
    .ts {{ color: #8b949e; font-size: 0.8rem; white-space: nowrap; }}
    .msg {{ font-family: monospace; color: #e6edf3; }}
    .vibe {{ color: #8b949e; font-style: italic; }}
    code {{ background: #21262d; padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; }}
    .footer {{ text-align: center; margin-top: 3rem; color: #484f58; font-size: 0.8rem; }}
    .footer a {{ color: #58a6ff; text-decoration: none; }}
  </style>
</head>
<body>
  <div class="header">
    <h1>📊 MoodGit</h1>
    <p>Emotional timeline of <strong>{repo_name}</strong> · Generated {generated_at}</p>
  </div>

  <div class="cards">
    <div class="card">
      <div class="val" style="color:{dom_color}">{dom_emoji}</div>
      <div class="val" style="color:{dom_color}; font-size:1.2rem">{dominant}</div>
      <div class="label">Dominant vibe</div>
    </div>
    <div class="card">
      <div class="val" style="color:#58a6ff">{summary["total_commits"]}</div>
      <div class="label">Commits analyzed</div>
    </div>
    <div class="card">
      <div class="val" style="color:#bc8cff">{summary["avg_intensity"]}</div>
      <div class="label">Avg intensity /10</div>
    </div>
    <div class="card">
      <div class="val" style="color:#f0883e">{summary["late_night_commits"]}</div>
      <div class="label">Late-night commits 🌙</div>
    </div>
  </div>

  <div class="chart-wrap">
    <h2>Emotion Breakdown</h2>
    <canvas id="emotionChart" height="260"></canvas>
  </div>

  <table>
    <thead>
      <tr>
        <th>Hash</th>
        <th>Time</th>
        <th>Emotion</th>
        <th>Intensity</th>
        <th>Message</th>
        <th>Vibe</th>
      </tr>
    </thead>
    <tbody>
      {commit_rows}
    </tbody>
  </table>

  <div class="footer">
    <p>Generated by <a href="https://github.com/Techie-Sakshi24/moodgit" target="_blank">MoodGit</a> 
    · your commits have feelings</p>
  </div>

  <script>
    const ctx = document.getElementById('emotionChart').getContext('2d');
    new Chart(ctx, {{
      type: 'doughnut',
      data: {{
        labels: {chart_labels},
        datasets: [{{
          data: {chart_data},
          backgroundColor: {chart_colors},
          borderColor: '#0d1117',
          borderWidth: 3,
        }}]
      }},
      options: {{
        plugins: {{
          legend: {{
            labels: {{ color: '#c9d1d9', font: {{ size: 13 }} }}
          }}
        }}
      }}
    }});
  </script>
</body>
</html>"""

    return html
