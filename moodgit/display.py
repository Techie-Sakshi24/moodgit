"""
MoodGit - Terminal display using Rich
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.columns import Columns
from rich.rule import Rule

console = Console()

EMOTION_STYLES = {
    "focused":      ("🎯", "bold cyan"),
    "stressed":     ("😤", "bold red"),
    "excited":      ("🚀", "bold yellow"),
    "tired":        ("😴", "dim blue"),
    "frustrated":   ("😤", "bold magenta"),
    "celebratory":  ("🎉", "bold green"),
    "confused":     ("🤔", "bold white"),
    "determined":   ("💪", "bold cyan"),
    "casual":       ("😎", "dim white"),
    "unknown":      ("❓", "dim"),
}

INTENSITY_BAR = "█"
INTENSITY_EMPTY = "░"


def intensity_bar(value: int, max_val: int = 10, width: int = 10) -> str:
    filled = int((value / max_val) * width)
    return INTENSITY_BAR * filled + INTENSITY_EMPTY * (width - filled)


def render_commits_table(analyzed: list):
    """Render commits as a rich table."""
    table = Table(
        title="[bold]Commit Emotional Timeline[/bold]",
        box=box.ROUNDED,
        show_lines=True,
        header_style="bold dim",
        border_style="dim",
    )

    table.add_column("Hash", style="dim", width=8)
    table.add_column("Timestamp", style="dim", width=17)
    table.add_column("Emotion", width=14)
    table.add_column("Intensity", width=14)
    table.add_column("Commit Message", width=35)
    table.add_column("Vibe", style="italic dim", width=40)

    for c in analyzed:
        emotion = c.get("emotion", "unknown")
        emoji, style = EMOTION_STYLES.get(emotion, ("❓", "dim"))
        intensity = c.get("intensity", 5)
        bar = f"[{style}]{intensity_bar(intensity)}[/{style}] {intensity}/10"

        table.add_row(
            f"[dim]{c.get('hash', '?')}[/dim]",
            f"[dim]{c.get('timestamp', '')}[/dim]",
            f"{emoji} [{style}]{emotion}[/{style}]",
            bar,
            Text(c.get("message", ""), overflow="ellipsis"),
            f"[italic dim]{c.get('vibe', '')}[/italic dim]",
        )

    console.print(table)


def render_summary(summary: dict, repo_name: str):
    """Render summary panel."""
    emotion = summary["dominant_emotion"]
    emoji, style = EMOTION_STYLES.get(emotion, ("❓", "dim"))
    counts = summary["emotion_counts"]

    # Build emotion breakdown
    emotion_lines = []
    for e, count in sorted(counts.items(), key=lambda x: -x[1]):
        em, st = EMOTION_STYLES.get(e, ("❓", "dim"))
        bar = intensity_bar(count, max(counts.values()), 8)
        emotion_lines.append(f"  {em} [{st}]{e:<12}[/{st}]  [dim]{bar}[/dim]  {count}")

    emotion_breakdown = "\n".join(emotion_lines)

    stressed_section = ""
    if summary.get("most_stressed_commit"):
        sc = summary["most_stressed_commit"]
        stressed_section = f"\n[bold red]💀 Peak stress commit:[/bold red] [dim]{sc['hash']}[/dim] — {sc['message'][:50]}"

    excited_section = ""
    if summary.get("most_excited_commit"):
        ec = summary["most_excited_commit"]
        excited_section = f"\n[bold green]🏆 Hype moment:[/bold green] [dim]{ec['hash']}[/dim] — {ec['message'][:50]}"

    late_night = summary["late_night_commits"]
    night_msg = f"[bold yellow]{late_night} late-night commits[/bold yellow] (11pm–4am)" if late_night > 0 else "No late-night commits found 😌"

    panel_content = f"""[bold]Repo:[/bold] {repo_name}
[bold]Commits analyzed:[/bold] {summary['total_commits']}
[bold]Dominant vibe:[/bold] {emoji} [{style}]{emotion}[/{style}]
[bold]Avg intensity:[/bold] {summary['avg_intensity']}/10

[bold]Emotion breakdown:[/bold]
{emotion_breakdown}

[bold]Late nights:[/bold] {night_msg}{stressed_section}{excited_section}"""

    console.print(Panel(
        panel_content,
        title="[bold]📊 MoodGit Summary[/bold]",
        border_style="cyan",
        padding=(1, 2),
    ))


def render_header():
    console.print()
    console.print(Rule("[bold cyan]MoodGit[/bold cyan] [dim]— your commits have feelings[/dim]"))
    console.print()


def render_footer():
    console.print()
    console.print(Rule("[dim]Made with 💙 by MoodGit — github.com/YOUR_USERNAME/moodgit[/dim]"))
    console.print()
